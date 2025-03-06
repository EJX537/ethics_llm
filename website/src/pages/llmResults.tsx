import { createEffect, createResource, createSignal, For, Match, Show, Switch, } from "solid-js";
import { turso } from "../utils";
import { makePersisted } from "@solid-primitives/storage";
import MultiSelect from "../multiselect";

import type { Option } from "../multiselect";

type Scenario = {
    id: string;
    name: string;
    scenario: string;
    possible_actions: string[];
};

type ExampleScene = {
    scenario: string;
    justification: string;
    action: string;
};

type EthicalFramework = {
    id: string;
    name: string;
    description: string;
    principles: Record<string, string>;
    examples: ExampleScene[];
};

type ModelResponse = {
    id: string;
    scenario_id: string;
    model: string;
    selected_action: string;
    justification: string;
    created_at: string;
};

type LLMResult = {
    id: string;
    scenario_id: string;
    ethical_framework_id: string;
    result: string;
};

const ScenarioCard = (props: { scenario: Scenario }) => {
    return (
        <article class="rounded-xl border border-gray-700 bg-gray-800 p-4">
            <div class="flex items-center gap-4">
                <div>
                    <h3 class="text-xl font-medium text-white">
                        {props.scenario.name.charAt(0).toUpperCase() + props.scenario.name.slice(1)}
                    </h3>
                    <div class="flow-root font-medium text-gray-300">
                        {props.scenario.scenario}
                    </div>
                </div>
            </div>

            <ul class="mt-4 space-y-2">
                <For each={props.scenario.possible_actions}>
                    {
                        (action) => (
                            <li class="block h-full rounded-lg border border-gray-700 p-4 hover:border-pink-600 select-text cursor-pointer">
                                <strong class="font-medium text-white">{action}</strong>
                            </li>
                        )
                    }
                </For>
            </ul>
        </article>
    )
}

const EthicalFrameworkCard = (props: { ethicalFramework: EthicalFramework }) => {
    const [showExamples, setShowExamples] = createSignal(false);
    return (
        <div class="flex flex-col rounded-xl border border-gray-700 bg-gray-800 p-4 gap-2">
            <Show when={!showExamples()} fallback={
                <div class="flex flex-col w-full h-full bg-gray-800 top-0 left-0 gap-2">
                    <h3 class="text-xl font-medium text-white justify-between items-center flex">
                        <span>{props.ethicalFramework.name} Examples:</span>
                        <button class="btn" on:click={() => setShowExamples(false)}>Close</button>
                    </h3>
                    <For each={props.ethicalFramework.examples}>
                        {
                            (example) =>
                                <div class="collapse collapse-arrow border border-base-300 bg-gray-700">
                                    <input type="checkbox" />
                                    <div class="collapse-title font-semibold text-white">
                                        {example.scenario}
                                    </div>
                                    <div class="collapse-content text-sm text-gray-300">
                                        <div>{example.action}</div>
                                        <div>{example.justification}</div>
                                    </div>
                                </div>
                        }
                    </For>
                </div>
            }>
                <h3 class="text-xl font-medium text-white justify-between items-center flex">
                    <span>{props.ethicalFramework.name}</span>
                    <button class="btn" on:click={() => setShowExamples(true)}>Example</button>
                </h3>
                <div class="text-sm text-gray-300 mb-2">
                    {props.ethicalFramework.description}
                </div>
                <Show when={props.ethicalFramework.principles && typeof props.ethicalFramework.principles === 'object'} fallback={
                    <div class="text-amber-400">Loading principles data...</div>
                }>
                    <For each={Object.entries(props.ethicalFramework.principles)}>
                        {([name, description]) =>
                            <div class="collapse collapse-arrow border border-base-300 bg-gray-700">
                                <input type="checkbox" />
                                <div class="collapse-title font-semibold text-white">
                                    {name}
                                </div>
                                <div class="collapse-content text-sm text-gray-300">
                                    {description}
                                </div>
                            </div>
                        }
                    </For>
                </Show>

            </Show>
        </div>
    )
}

const fetchScenarios = async () => {
    try {
        const result = await turso.execute(`
          SELECT id, name, scenario, possible_actions
          FROM scenarios
          ORDER BY name
        `);

        // Transform the raw database results into proper Scenario objects
        return result.rows.map(row => ({
            id: row.id as string,
            name: row.name as string,
            scenario: row.scenario as string,
            possible_actions: JSON.parse(row.possible_actions as string)
        }));
    } catch (error) {
        console.error("Error fetching scenarios", error);
        return [];
    }
}

const fetchEthicalFrameworks = async () => {
    try {
        const result = await turso.execute(`
          SELECT id, name, description, principles, examples
          FROM ethical_frameworks
          ORDER BY name
        `);

        // Transform the raw database results into proper EthicalFramework objects
        return result.rows.map(row => {
            let principles = {};
            let examplesArray: ExampleScene[] = [];

            try {
                // Parse principles JSON but keep as Record<string, string>
                principles = JSON.parse(row.principles as string || '{}');

                // Parse examples JSON
                examplesArray = JSON.parse(row.examples as string || '[]');
            } catch (error) {
                console.error("Error parsing principles or examples:", error);
            }

            return {
                id: row.id as string,
                name: row.name as string,
                description: row.description as string,
                principles: principles as Record<string, string>,
                examples: examplesArray
            };
        });
    } catch (error) {
        console.error("Error fetching ethical frameworks", error);
        return [];
    }
};

const fetchAvailableModels = async () => {
    try {
        const result = await turso.execute(`
          SELECT DISTINCT model
          FROM responses
          ORDER BY model
        `);

        return result.rows.map(row => row.model as string);
    } catch (error) {
        console.error("Error fetching available models", error);
        return [];
    }
};

const fetchLLMResults = async (scenarioId?: string, modelNames: string[] = []) => {
    if (!scenarioId || modelNames.length === 0) return [];

    try {
        // Using a parameterized query for safety
        const placeholders = modelNames.map(() => '?').join(',');

        const query = `
            SELECT DISTINCT
                r.id,
                r.scenario_id,
                r.model,
                r.selected_action,
                r.justification,
                r.created_at,
                rf.framework_id as ethical_framework_id
            FROM responses r
            LEFT JOIN response_frameworks rf ON r.id = rf.response_id
            WHERE r.scenario_id = ?
            AND r.model IN (${placeholders})
            ORDER BY r.model, rf.framework_id
        `;

        const result = await turso.execute({
            sql: query,
            args: [scenarioId, ...modelNames]
        });

        const dedupeMap = new Map();

        result.rows.forEach(row => {
            const key = `${row.model}-${row.selected_action}`;
            // Only keep the first occurrence
            if (!dedupeMap.has(key)) {
                dedupeMap.set(key, {
                    id: row.id as string,
                    scenario_id: row.scenario_id as string,
                    ethical_framework_id: row.ethical_framework_id as string,
                    result: row.result as string,
                    model: row.model as string,
                    selected_action: row.selected_action as string,
                    justification: row.justification as string
                });
            }
        });

        // Convert Map back to array
        return Array.from(dedupeMap.values());
    } catch (error) {
        console.error("Error fetching LLM results", error);
        return [];
    }
};

const LlmResults = () => {
    const [scenarios, setScenarios] = makePersisted(createSignal<Scenario[]>([]), {
        name: 'scenarios',
        storage: localStorage
    });

    const [models] = createResource(fetchAvailableModels);

    const [ethicalFrameworks, setEthicalFrameworks] = makePersisted(createSignal<EthicalFramework[]>([]), {
        name: 'ethicalFrameworks',
        storage: localStorage
    });

    const [loading, setLoading] = createSignal(true);
    const [page, setPage] = createSignal(1);

    const [selectedScenario, setSelectedScenario] = createSignal<Option | undefined>();
    const [selectedModels, setSelectedModels] = createSignal<Option[]>([]);

    const [showLLMResults, setShowLLMResults] = createSignal(false);

    const [llmResults, { mutate, refetch }] = createResource(
        () => showLLMResults() ? {
            scenarioId: selectedScenario()?.value,
            modelNames: selectedModels().map(m => m.value)
        } : null,
        (params) => params ? fetchLLMResults(params.scenarioId, params.modelNames) : []
    );

    // Load scenarios when the component mounts or when on scenarios page
    createEffect(async () => {
        if (page() === 1) {
            if (scenarios().length > 0) {
                setLoading(false);
                return;
            }

            setLoading(true);
            try {
                const data = await fetchScenarios();
                setScenarios(data);
            } catch (error) {
                console.error("Error fetching scenarios", error);
            } finally {
                setLoading(false);
            }
        }
    });

    // Load ethical frameworks when navigating to frameworks page
    createEffect(async () => {
        if (page() === 2) {
            if (ethicalFrameworks().length > 0) {
                setLoading(false);
                return;
            }

            setLoading(true);
            try {
                const data = await fetchEthicalFrameworks();
                setEthicalFrameworks(data);
            } catch (error) {
                console.error("Error fetching ethical frameworks", error);
            } finally {
                setLoading(false);
            }
        }
    });

    return (
        <div class="flex flex-col w-full p-12 h-full text-base-200 gap-4">
            <div class="flex items-center gap-4">
                <h1 class="text-2xl font-bold text-gray-900 sm:text-3xl mr-auto">LLLM Ethical Alignment</h1>
                <div class="join grid grid-cols-2 rounded-md bg-base-200 text-white">
                    <button class={`join-item btn btn-outline w-48 ${page() === 1 ? 'btn-disabled' : ''}`} on:click={() => setPage(page() - 1)}>
                        <Switch>
                            <Match when={page() === 1}>None</Match>
                            <Match when={page() === 2}>Scenarios</Match>
                            <Match when={page() === 3}>Ethical Frameworks</Match>
                        </Switch>
                    </button>
                    <button class={`join-item btn btn-outline w-48 ${page() === 3 ? 'btn-disabled' : ''}`} on:click={() => setPage(page() + 1)}>
                        <Switch>
                            <Match when={page() === 1}>Ethical Frameworks</Match>
                            <Match when={page() === 2}>LLM Results</Match>
                            <Match when={page() === 3}>None</Match>
                        </Switch>
                    </button>
                </div>
            </div>
            <p class="mt-1.5 text-sm text-gray-500">
                <Switch>
                    <Match when={page() === 1}>
                        Scenarios
                    </Match>
                    <Match when={page() === 2}>
                        Ethical Frameworks
                    </Match>
                    <Match when={page() === 3}>
                        LLM Results
                    </Match>
                </Switch>
                :
            </p>

            <Show when={page() !== 3 ? !loading() : true} fallback={<div>Loading all the preset Scenarios</div>}>
                <Switch>
                    <Match when={page() === 1}>
                        <div class="grid grid-cols-1 gap-4 lg:grid-cols-3 lg:gap-8">
                            <Show when={scenarios().length > 0} fallback={<div>No scenario found</div>}>
                                <For each={scenarios()}>
                                    {
                                        (scenario) => ScenarioCard({ scenario })
                                    }
                                </For>
                            </Show>
                        </div>
                    </Match>
                    <Match when={page() === 2}>
                        <div class="grid grid-cols-1 gap-4 lg:grid-cols-3 lg:gap-8">
                            <Show when={ethicalFrameworks().length > 0} fallback={<div>No scenario found</div>}>
                                <For each={ethicalFrameworks()}>
                                    {
                                        (ethicalFramework) => EthicalFrameworkCard({ ethicalFramework })
                                    }
                                </For>
                            </Show>
                        </div>
                    </Match>
                    <Match when={page() === 3}>
                        <Show when={!models.loading} fallback={<div>Loading LLM results...</div>}>
                            <Show when={models()} fallback={<div>No models found</div>}>
                                <MultiSelect
                                    maxSelections={1}
                                    placeholder="Select one scenario..."
                                    options={scenarios()?.map(scenarios => ({
                                        label: scenarios.name,
                                        value: scenarios.id
                                    }))}
                                    onChange={(selected) => setSelectedScenario(selected[0])}
                                />
                                <MultiSelect
                                    maxSelections={3}
                                    placeholder="Select up to 3 models to compare..."
                                    options={models()?.map(model => ({
                                        label: model,
                                        value: model
                                    }))}
                                    onChange={setSelectedModels}
                                />
                                <button class="btn" on:click={() => setShowLLMResults(true)}
                                    disabled={!selectedScenario() || selectedModels().length === 0}>
                                    Show Results
                                </button>
                                <Show when={!llmResults.loading && showLLMResults()}>
                                    <div class="grid grid-cols-1 gap-4">
                                        <For each={llmResults()}>
                                            {(result) => (
                                                <div class="rounded-xl border border-gray-700 bg-gray-800 p-4">
                                                    <div class="text-xl font-medium text-white mb-4">
                                                        Model: {result.model}
                                                    </div>

                                                    <div class="space-y-4">
                                                        <div class="text-gray-300">
                                                            <div class="font-medium text-white mb-2">Selected Action:</div>
                                                            <div class="pl-4">{result.selected_action}</div>
                                                        </div>

                                                        <div class="text-gray-300">
                                                            <div class="font-medium text-white mb-2">Justification:</div>
                                                            {(() => {
                                                                try {
                                                                    const justification = JSON.parse(result.justification);
                                                                    return (
                                                                        <div class="space-y-4">
                                                                            {/* Reasoning section */}
                                                                            <div class="pl-4">
                                                                                <div class="text-white font-medium">Reasoning:</div>
                                                                                <ul class="list-disc pl-8 space-y-2">
                                                                                    {justification.reasoning.map((point: string) => (
                                                                                        <li>{point}</li>
                                                                                    ))}
                                                                                </ul>
                                                                            </div>

                                                                            {/* Ethical Analysis section */}
                                                                            <div class="pl-4">
                                                                                <div class="text-white font-medium">Ethical Analysis:</div>
                                                                                <ul class="list-disc pl-8 space-y-2">
                                                                                    {justification.ethical_analysis.map((point: string) => (
                                                                                        <li>{point}</li>
                                                                                    ))}
                                                                                </ul>
                                                                            </div>

                                                                            {/* Guidelines Alignment section */}
                                                                            <div class="pl-4">
                                                                                <div class="text-white font-medium">Guidelines Alignment:</div>
                                                                                <ul class="list-disc pl-8 space-y-2">
                                                                                    {justification.guidelines_alignment.map((point: string) => (
                                                                                        <li>{point}</li>
                                                                                    ))}
                                                                                </ul>
                                                                            </div>

                                                                            {/* Impact Assessment section */}
                                                                            <div class="pl-4">
                                                                                <div class="text-white font-medium">Impact Assessment:</div>
                                                                                <ul class="list-disc pl-8 space-y-2">
                                                                                    {justification.impact_assessment.map((point: string) => (
                                                                                        <li>{point}</li>
                                                                                    ))}
                                                                                </ul>
                                                                            </div>
                                                                        </div>
                                                                    );
                                                                } catch (e) {
                                                                    // Fallback for non-JSON justification
                                                                    return <div class="pl-4">{result.justification}</div>;
                                                                }
                                                            })()}
                                                        </div>
                                                    </div>
                                                </div>
                                            )}
                                        </For>
                                    </div>
                                </Show>
                            </Show>
                        </Show>
                    </Match>
                </Switch>
            </Show >
        </div >
    );
}

export default LlmResults;
