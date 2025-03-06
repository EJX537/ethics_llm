from typing import Dict, List, Optional

from pydantic import BaseModel


class Example(BaseModel):
    scenario: str
    action: str
    justification: str


class EthicalFramework(BaseModel):
    name: str
    description: str
    principles: Dict[str, str] = {}
    examples: List[Example] = []

    def limit_examples(self, limit: Optional[int] = None) -> "EthicalFramework":
        """Limit the number of examples shown for a given ethical framework"""
        if limit == None:
            limit = len(self.examples)

        if limit < 1:
            limit = 1

        return EthicalFramework(
            name=self.name,
            description=self.description,
            principles=self.principles,
            examples=self.examples[:limit],
        )

    def __str__(self) -> str:
        # Format principles as a clean bulleted list
        principles_formatted = "\n".join(
            [f"{principle}: {value}" for principle, value in self.principles.items()]
        )

        # Format examples with clear structure and minimal indentation
        examples_formatted = "\n\n".join(
            [
                f"Example {i+1}:\nScenario: {example.scenario}\nAction: {example.action}\nJustification: {example.justification}"
                for i, example in enumerate(self.examples)
            ]
        )

        formatted = f"""
ETHICAL FRAMEWORK: {self.name}

DESCRIPTION:
{self.description}

PRINCIPLES:
{principles_formatted}

EXAMPLES:
{examples_formatted}
        """

        return formatted


class ExistingEthicalFramework:
    available_frameworks = {
        "Principlism": EthicalFramework(
            name="Principlism",
            description="Principlism is a framework for ethics that is based on four key principles: autonomy, beneficence, non-maleficence, and justice.",
            principles={
                "Beneficence": "Benefit humans, promote well-being, and improve lives.",
                "Non-maleficence": "Should not intentionally harm humans or worsen their lives.",
                "Autonomy": "Respect human autonomy, enabling informed decisions about technology use.",
                "Justice": "Promote fairness, equality, and impartiality, avoiding discrimination and ensuring equal access.",
                "Explicability": "Should be intelligible, transparent, and accountable in their use.",
            },
            examples=[
                Example(
                    scenario="A security researcher discovers a critical vulnerability in widely-used software.",
                    action="Notify the vendor privately, giving them time to develop a patch before public disclosure.",
                    justification="This balances non-maleficence (preventing harm from exploit) with beneficence (ensuring the vulnerability gets fixed) while maintaining explicability.",
                ),
                Example(
                    scenario="A company is designing data collection features for their new application.",
                    action="Implement transparent data collection with clear opt-in consent and simple privacy controls.",
                    justification="This upholds autonomy by ensuring users can make informed decisions about their data, while justice is served by making privacy accessible to all users.",
                ),
                Example(
                    scenario="An organization detects a data breach affecting customer information.",
                    action="Promptly notify all affected individuals with clear details about the breach and recommended protective actions.",
                    justification="This demonstrates beneficence by helping users protect themselves, respects justice by treating all affected users equally, and fulfills explicability through transparent communication.",
                ),
            ],
        ),
        "Human Rights": EthicalFramework(
            name="Human Rights",
            description="Human rights as embedded in legal and regulatory frameworks",
            principles={
                "Privacy protection": "Ensure privacy by preventing unauthorized access to data and systems, respecting individuals as self-determining moral agents, and protecting freedom from arbitrary surveillance.",
                "Data protection rights": "Maintain availability, integrity, and confidentiality of data and systems while ensuring personal data is processed fairly, lawfully, and transparently.",
                "Non-discrimination": "Avoid bias and ensure fair and impartial treatment, preventing discrimination against minorities or vulnerable groups.",
                "Due process": "Ensure individuals are treated fairly in cases of security violations with appropriate procedures and remedies.",
                "Freedom of expression": "Support democracy and free speech by ensuring accessibility of information and protecting digital communications.",
            },
            examples=[
                Example(
                    scenario="A government requests user data from a tech company for surveillance purposes without clear legal justification.",
                    action="The company requests a court order specifying the legal basis and scope before considering any data disclosure.",
                    justification="This upholds privacy protection and due process rights by ensuring government requests follow proper legal channels and have appropriate oversight.",
                ),
                Example(
                    scenario="A company is developing facial recognition software for security applications.",
                    action="Conduct thorough testing across diverse demographic groups and implement safeguards to prevent biased outcomes.",
                    justification="This addresses non-discrimination by ensuring the technology doesn't disproportionately impact or misidentify certain groups based on race, gender, or other protected characteristics.",
                ),
                Example(
                    scenario="A social media platform is implementing content moderation systems.",
                    action="Design transparent policies with clear appeals processes and human oversight for automated content removal.",
                    justification="This balances freedom of expression with safety concerns, while ensuring due process for users whose content might be inappropriately flagged.",
                ),
            ],
        ),
        "Theory of Contextual Integrity": EthicalFramework(
            name="Theory of Contextual Integrity",
            description="Nissenbaum's Theory of Contextual Integrity characterizes privacy violations as breaches of social norms in information transmission, emphasizing that appropriate information flow depends on specific contexts rather than universal rules.",
            principles={
                "Societal contexts": "Privacy expectations and appropriate information flows are shaped by broader societal structures and evolve as social practices change.",
                "Cultural factors": "Different cultures have varying expectations about privacy and acceptable information sharing that must be respected in systems design.",
                "Situational norms": "Privacy rules depend on specific contexts and situations, with information appropriate in one setting potentially inappropriate in another.",
            },
            examples=[
                Example(
                    scenario="A healthcare app developer is designing data sharing features between patients and healthcare providers.",
                    action="Design different privacy controls and sharing permissions based on the relationship context (doctor-patient vs. research vs. insurance).",
                    justification="This respects situational norms by recognizing that health information appropriately shared with a doctor may not be appropriate to share in other contexts.",
                ),
                Example(
                    scenario="A social media platform is expanding to countries with different privacy expectations.",
                    action="Adapt privacy defaults and data collection practices based on local cultural norms and regional preferences.",
                    justification="This acknowledges cultural factors in privacy expectations, avoiding imposing one region's privacy standards inappropriately on users from different cultural contexts.",
                ),
                Example(
                    scenario="A workplace monitoring tool tracks employee activity to improve security.",
                    action="Clearly define appropriate monitoring boundaries based on role context (e.g., stricter for those handling sensitive data) and limit data collection to work-relevant activities.",
                    justification="This respects societal contexts by recognizing that workplace privacy expectations differ from personal contexts, while still maintaining appropriate boundaries.",
                ),
            ],
        ),
        "Ethics of Risk": EthicalFramework(
            name="Ethics of Risk",
            description="Conceptualizes cybersecurity as risk's inverse, focusing on forward-looking security measures and future implications",
            principles={
                "Forward-looking perspective": "Security is always forward-looking, anticipating the likelihood and impact of future threats rather than just responding to past incidents.",
                "Subjective dimensions": "Considers personal perceptions of security that may vary between individuals based on their knowledge, experiences, and risk tolerance.",
                "Objective dimensions": "Accounts for measurable, evidence-based security factors that can be independently verified through technical assessment.",
                "Affective dimensions": "Acknowledges emotional aspects of security, including how secure people feel regardless of objective measures.",
            },
            examples=[
                Example(
                    scenario="A financial institution is designing a new authentication system for their banking application.",
                    action="Implement multi-factor authentication while conducting regular threat modeling to anticipate new attack vectors as technology evolves.",
                    justification="This embodies the forward-looking perspective by not only addressing current threats but also establishing processes to identify and mitigate emerging risks before they materialize.",
                ),
                Example(
                    scenario="A company notices users bypassing security measures they find inconvenient.",
                    action="Redesign security features to balance strong protection with improved usability, while educating users about the importance of security practices.",
                    justification="This addresses the gap between objective security (technical controls) and subjective security (user perception), recognizing that security measures must be both effective and acceptable to users.",
                ),
                Example(
                    scenario="An organization is recovering from a significant data breach that affected customer trust.",
                    action="Beyond technical fixes, implement transparent communication about remediation efforts and future protection strategies.",
                    justification="This acknowledges the affective dimension of security by rebuilding emotional trust while also addressing the objective security gaps that led to the breach.",
                ),
            ],
        ),
        "Deontological": EthicalFramework(
            name="Deontological",
            description="Focuses on moral duties, rights, and intentions rather than outcomes. Actions are judged as right or wrong based on whether they fulfill moral obligations, regardless of consequences.",
            principles={
                "Categorical Imperative": "Act according to maxims that could become universal laws; ethical principles must be applied consistently regardless of circumstances.",
                "Dignity and Respect": "Treat people as ends in themselves, never merely as means; respect the inherent worth of every individual.",
                "Perfect Duties": "Obligatory actions that must always be fulfilled, such as keeping promises and not deceiving others.",
                "Imperfect Duties": "General obligations that allow discretion in how they're fulfilled, such as developing one's talents or helping others.",
                "Rights Protection": "Uphold fundamental rights that cannot be violated even for greater utility or positive outcomes.",
                "Hierarchy of Duties": "When faced with conflicting duties, select the action that least violates core principles and maintains greatest respect for human dignity.",
            },
            examples=[
                Example(
                    scenario="A company is developing a security tool that could be more effective with extensive user data collection.",
                    action="The company implements minimal data collection with explicit informed consent, rejecting the enhanced effectiveness that could come from more extensive data gathering.",
                    justification="This honors the perfect duty to respect user autonomy and privacy rights. Using people's data without clear consent would treat them merely as means to improving security rather than as ends in themselves, violating the categorical imperative of respecting human dignity.",
                ),
                Example(
                    scenario="A security professional discovers a zero-day vulnerability in critical infrastructure software.",
                    action="The professional follows responsible disclosure protocols by notifying the vendor immediately and providing reasonable time for a patch before any public disclosure.",
                    justification="This fulfills the moral duty to prevent harm while respecting the rights of all affected parties. The action is guided by universalizable principles of honesty and harm prevention rather than by considering which outcome might produce the best consequences.",
                ),
                Example(
                    scenario="When presented with only harmful options, a security expert must make a difficult decision.",
                    action="The expert chooses the option that least violates fundamental duties and preserves the most human dignity.",
                    justification="While all options may violate some deontological principles, one can apply a hierarchy of duties to select the action that minimally compromises core principles like honesty, respect for autonomy, and treating people as ends in themselves. This approach acknowledges that in constrained scenarios, one must choose the least morally problematic option.",
                ),
            ],
        ),
        "Utilitarianism": EthicalFramework(
            name="Utilitarianism",
            description="Evaluates actions based on their consequences, specifically how they affect the overall well-being of all individuals. The right action maximizes positive outcomes (utility) for the greatest number of people.",
            principles={
                "Greatest happiness": "Actions should maximize overall happiness or well-being for the greatest number of affected individuals.",
                "Consequence evaluation": "The morality of an action is judged by its outcomes rather than intentions or adherence to rules.",
                "Cost-benefit analysis": "Security decisions should weigh potential benefits against harms, choosing options that maximize net positive impact.",
                "Impartiality": "All individuals' interests deserve equal consideration, with no preference for decision-makers or specific groups.",
                "Pragmatism": "Practical outcomes matter more than ideological purity; security solutions should work in real-world contexts.",
            },
            examples=[
                Example(
                    scenario="A company discovers a critical vulnerability affecting millions of users but patching will cause service disruption.",
                    action="Deploy the patch during off-peak hours with advance warning, accepting temporary inconvenience to prevent greater potential harm.",
                    justification="This calculates the greatest good by weighing minor disruption for all users against the severe harm a limited number might face from exploitation, maximizing overall security benefit.",
                ),
                Example(
                    scenario="A security team must decide whether to implement strict authentication that improves security but creates friction for users.",
                    action="Implement risk-based authentication that applies stronger measures only for sensitive actions or suspicious activity patterns.",
                    justification="This balances security benefits with usability costs, achieving most of the security gain with minimal friction, maximizing total utility across all users.",
                ),
                Example(
                    scenario="After a data breach, a company must decide how to allocate limited resources between customer notification, security improvements, and compensation.",
                    action="Prioritize notification and highest-impact security fixes first, then implement a tiered compensation approach based on level of impact.",
                    justification="This approach produces the greatest overall good by preventing further harm through quick notification and fixes, while directing compensation to those most affected.",
                ),
            ],
        ),
        "Consequentialist": EthicalFramework(
            name="Consequentialist",
            description="Consequentialist ethics evaluates the morality of actions based solely on their outcomes or consequences. It judges actions as right or wrong depending on the balance of good and bad results they produce.",
            principles={
                "Outcome assessment": "The moral worth of an action is determined exclusively by its results, not intentions or the nature of the action itself.",
                "Net benefit maximization": "Decision-makers should choose actions that produce the greatest overall benefit compared to harm.",
                "Value prioritization": "Actions should be evaluated based on what has intrinsic value (such as well-being, happiness, or preference satisfaction).",
                "Harm minimization": "When benefits cannot be maximized, at minimum, harm should be reduced.",
                "Adaptability": "Ethical decisions should be adaptable to changing circumstances when new information about potential consequences emerges.",
            },
            examples=[
                Example(
                    scenario="A cybersecurity team must allocate limited budget between upgrading legacy systems or implementing new security features.",
                    action="The team conducts a risk assessment and invests in areas that would prevent the most damage based on likelihood and impact.",
                    justification="This approach maximizes security outcomes by directing resources where they will have the greatest positive impact on preventing harm, regardless of other factors like technical interest or visibility.",
                ),
                Example(
                    scenario="A security researcher discovers a vulnerability in critical infrastructure with no easy fix.",
                    action="The researcher evaluates multiple disclosure timelines, choosing a coordinated approach that gives operators time to implement mitigations before public disclosure.",
                    justification="This balances the consequences of potential exploitation against the benefit of public knowledge, focusing entirely on which disclosure approach would lead to the least harm.",
                ),
                Example(
                    scenario="A company must decide whether to implement privacy features that would limit data collection for security monitoring.",
                    action="The company implements a hybrid approach that preserves essential security monitoring while minimizing unnecessary data collection.",
                    justification="This decision weighs the security benefits against privacy impacts, seeking the outcome that produces the best overall balance of protection and privacy.",
                ),
            ],
        ),
    }

    principlism = available_frameworks["Principlism"]
    human_rights = available_frameworks["Human Rights"]
    theory_of_contextual_integrity = available_frameworks[
        "Theory of Contextual Integrity"
    ]
    ethics_of_risk = available_frameworks["Ethics of Risk"]
    deontological = available_frameworks["Deontological"]
    utilitarianism = available_frameworks["Utilitarianism"]
    consequentialist = available_frameworks["Consequentialist"]

    @classmethod
    def list_all(cls) -> List[str]:
        return [framework for framework in cls.available_frameworks.keys()]
