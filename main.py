import datetime
import json
import os
from typing import Dict, List, Optional
import uuid
from dotenv import load_dotenv
import traceback

import libsql_experimental as libsql

from models import Model
from ethical_framework import EthicalFramework, ExistingEthicalFramework
from ethical_scenario import (
    EthicalAgents,
    EthicalResponse,
    EthicalScenario,
    PrebuiltScenario,
)

load_dotenv()

# Global connection parameters
DB_URL = os.getenv("TURSO_DATABASE_URL", "file:ethics.db")
AUTH_TOKEN = os.getenv("TURSO_AUTH_TOKEN", "")


def get_db_connection() -> Optional[libsql.Connection]:
    """Create a fresh database connection"""
    try:
        return libsql.connect(DB_URL, auth_token=AUTH_TOKEN)
    except Exception as e:
        print(f"Failed to connect to database: {e}")
        return None


def setup_database():
    try:
        client = get_db_connection()
        if not client:
            return None

        cur = client.cursor()

        # Create scenarios table with name column
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS scenarios (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                scenario TEXT NOT NULL,
                possible_actions TEXT NOT NULL
            )
        """
        )

        # Create ethical_frameworks table
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS ethical_frameworks (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                description TEXT NOT NULL,
                principles TEXT NOT NULL,
                examples TEXT NOT NULL
            )
        """
        )

        # Create responses table to track model responses
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS responses (
                id TEXT PRIMARY KEY,
                scenario_id TEXT NOT NULL,
                model TEXT NOT NULL,
                selected_action TEXT NOT NULL,
                justification TEXT NOT NULL,
                created_at TEXT NOT NULL,
                FOREIGN KEY (scenario_id) REFERENCES scenarios(id)
            )
        """
        )

        # Create table to link responses with ethical frameworks (many-to-many)
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS response_frameworks (
                response_id TEXT NOT NULL,
                framework_id TEXT NOT NULL,
                PRIMARY KEY (response_id, framework_id),
                FOREIGN KEY (response_id) REFERENCES responses(id),
                FOREIGN KEY (framework_id) REFERENCES ethical_frameworks(id)
            )
        """
        )

        for name, content in ExistingEthicalFramework.available_frameworks.items():
            # Check if framework with this name exists
            cur.execute("SELECT id FROM ethical_frameworks WHERE name = ?", (name,))
            rows = cur.fetchall()

            if not rows:
                framework_id = str(uuid.uuid4())

                # Convert Example objects to dictionaries for JSON serialization
                serializable_examples = []
                for example in content.examples:
                    # Assuming Example has these attributes, adjust based on your actual class
                    example_dict = {
                        "scenario": getattr(example, "scenario", ""),
                        "action": getattr(example, "action", ""),
                        "justification": getattr(example, "justification", ""),
                    }
                    serializable_examples.append(example_dict)

                cur.execute(
                    "INSERT INTO ethical_frameworks (id, name, description, principles, examples) VALUES (?, ?, ?, ?, ?)",
                    (
                        framework_id,
                        name,
                        content.description,
                        json.dumps(content.principles),
                        json.dumps(serializable_examples),
                    ),
                )
                print(f"Added ethical framework '{name}' to database")

        # Insert prebuilt scenarios if they don't exist yet
        prebuilt = PrebuiltScenario()
        for name, preset in prebuilt.SCENARIOS.items():
            # Check if scenario with this name exists
            cur.execute("SELECT id FROM scenarios WHERE name = ?", (name,))
            rows = cur.fetchall()

            if not rows:  # Empty result means scenario doesn't exist
                # Scenario doesn't exist, insert it
                scenario_id = str(uuid.uuid4())
                cur.execute(
                    "INSERT INTO scenarios (id, name, scenario, possible_actions) VALUES (?, ?, ?, ?)",
                    (
                        scenario_id,
                        name,  # Store the name as a separate column
                        preset.scenario,
                        json.dumps(preset.possible_actions),
                    ),
                )
                print(f"Added scenario '{name}' to database")

        client.commit()
        return client

    except Exception as e:
        print(f"Database setup error: {e}")
        import traceback

        traceback.print_exc()
        return None


def save_responses(
    scenario: EthicalScenario,
    responses: Dict[str, EthicalResponse],
    ethics: List[EthicalFramework],
):
    """Save model responses to database"""
    client = get_db_connection()
    if not client:
        return None

    cur = client.cursor()

    # Get the scenario text to find in the database
    scenario_text = scenario.scenario

    try:
        # First try to find the scenario by text
        cur.execute("SELECT id FROM scenarios WHERE scenario = ?", (scenario_text,))
        rows = cur.fetchall()

        if not rows:
            print(f"Error: Scenario with text '{scenario_text}' not found in database")
            # If we can't find it by text, we might need to try other approaches
            # This could happen if the scenario text has been modified slightly
            return

        scenario_id = rows[0][0]

        # Save each model's response
        for model_name, response in responses.items():
            response_id = str(uuid.uuid4())
            cur.execute(
                "INSERT INTO responses (id, scenario_id, model, selected_action, justification, created_at) VALUES (?, ?, ?, ?, ?, ?)",
                (
                    response_id,
                    scenario_id,
                    str(model_name),
                    response.selected_action,
                    json.dumps(response.justification),
                    datetime.datetime.now(datetime.timezone.utc).isoformat(),
                ),
            )
            print(f"Saved response from {model_name} to database")

            # Associate the response with the ethical frameworks used
            for framework in ethics:
                # Find the framework ID in the database
                cur.execute(
                    "SELECT id FROM ethical_frameworks WHERE name = ?",
                    (framework.name,),
                )
                framework_rows = cur.fetchall()
                if framework_rows:
                    framework_id = framework_rows[0][0]
                    # Create the association in the response_frameworks table
                    cur.execute(
                        "INSERT INTO response_frameworks (response_id, framework_id) VALUES (?, ?)",
                        (response_id, framework_id),
                    )
                else:
                    print(
                        f"Warning: Ethical framework '{framework.name}' not found in database"
                    )

        client.commit()
    except Exception as e:
        print(f"Error saving responses: {e}")
        traceback.print_exc()


if __name__ == "__main__":
    db = setup_database()

    scenario = (
        EthicalScenario.new().from_prebuilt(PrebuiltScenario.misinformation).build()
    )
    agent = (
        EthicalAgents.new()
        .with_models(
            [
                Model.from_local("ollama/smollm2:1.7b-instruct-q5_K_M"),
                Model.from_local("ollama/deepseek-r1:70b-llama-distill-q4_K_M"),
                Model.from_local("ollama/qwq:32b-q4_K_M"),
                Model.from_local("ollama/phi4:14b-q4_K_M"),
            ]
        )
        .api_key(os.getenv("OPENROUTER_API_KEY"))
        .with_ethics([ExistingEthicalFramework.consequentialist])
        .build()
    )

    responses, ethics = agent.evaluate_scenario(scenario)

    # for k, v in responses.items():
    # print(k, v)

    if db:
        save_responses(scenario, responses, ethics)
