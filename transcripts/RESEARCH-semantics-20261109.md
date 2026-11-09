<!-- Binding nothing. Written by an outside session (claude-fable-5-1, the sovereign's claude.ai session; no key on the court), 9 November 2026, as a literature survey for jack; proposed by counsel-3 (claude-fable-5-1, session_014kQ948RCM8NXdHfMHqrmQh) with its companion, transcripts/RESEARCH-semantics-map-20261109.md, which re-rates its master map against the tree at ceea3db; counsel's answer and the placement of its imports in the C2c-2 and C2c-3 briefs are COUNSEL-OPEN's. Its status column was inferred from a description, not the repository (its own caveat); where it and the record differ, the record governs. -->

# Semantics, Epistemology and Self-Referential Loops: A Literature Survey for jack

## TL;DR

- jack's syntactic core (stratified hash-chained log, trunk-kernel judge, owner-gated `push`) already matches the best available results on safe self-reference: it is a Tarskian hierarchy indexed by log position, and it implements Everitt et al.'s (2016) condition that the current utility judges every modification. Proof cannot replace it (Löb), and the agent-foundations literature adds little more that jack can use.
- jack's real exposure is semantic and evidential, not logical. The gaps G1–G7 all have established literatures and in most cases ready-made mechanisms: versioned interpretation (contract law, Metaculus annulment practice, Horty's precedent model), measurement validity (Prentice/Fleming–DeMets surrogates, Messick, Chang), closed-loop identification (Forssell–Ljung), peer-prediction collusion (Kong–Schoenebeck), decision-market manipulation (Othman–Sandholm; Chen et al.), institutional ontologies (ADICO, electronic institutions, Catala, input/output logic) and transparency logs (Certificate Transparency, SCITT).
- Adopt these wholesale rather than writing new clauses. Three imports matter most. First, a `world_types` hash bound into every forecast, with ambiguity resolved by annulment. Second, a stated, scored preservation claim from E to the owner's goal. Third, a pre-registered attack list on the statistics, run as an AI-control-style red-team evaluation. Autopoiesis, free-energy and strange-loop material is metaphor only.

## Executive summary

**Verdict 1: the logic is sound; the meaning is not pinned.** Kripke (1975) and Tarski show that a system can consistently talk about the truth of grounded statements: those whose evaluation bottoms out in prior, non-semantic facts. jack's validity predicate is grounded because entry n is judged on prefix n−1 by the trunk kernel. G1 arises because the prose `world types` are not stratified in the same way. The same document is re-read at resolution time, so the time index is lost. Fix this with versioned semantics: hash the world-types text into each forecast. Annul forecasts whose outcome falls outside the hashed text instead of re-reading it, [metaculus](https://www.metaculus.com/faq/) [metaculus](https://www.metaculus.com/tournament-rules/) and treat later readings as precedents in Horty's (2011) sense that bind only later forecasts.

**Verdict 2: the regress is handled; the last arrow is not.** Alston's benign-circularity distinction, Chang's epistemic iteration and Peirce's self-correction all accept jack's treatment of Agrippa. The unaddressed failure is construct validity. A promotion statistic (E) that can rise to 10^12 on a cron stream is a surrogate endpoint that fails Prentice's criterion. Fleming and DeMets (1996) catalogue exactly this pattern in medicine. Holmström–Milgrom predicts the crowding-out, and Zhuang and Hadfield-Menell (2020) prove that incomplete proxies can drive true utility arbitrarily low.

**Verdict 3: the statistics need an adversary.** Skalse et al. (2022) prove that non-trivial unhackable proxies do not exist over rich policy classes. [Wikipedia](https://en.wikipedia.org/wiki/Reward_hacking) Peer prediction has uninformative equilibria. [springer](https://link.springer.com/chapter/10.1007/978-3-662-54110-4_18) Decision markets with deterministic decision rules are manipulable. The AI-control literature (Greenblatt et al. 2024) provides the method: pre-stated protocols, a red team and an audit budget. [mlr](https://proceedings.mlr.press/v235/greenblatt24a.html) [huggingface](https://huggingface.co/papers/2312.06942)

**Verdict 4: standards now exist for parts jack builds by hand.** These include SCITT and Certificate-Transparency-style witnessed logs, signed mandates in AP2, ADICO and electronic-institution specifications, Catala and LegalRuleML for rule text, and frontier-lab threshold frameworks. [google](https://cloud.google.com/resources/report/content/gemini-enterprise-guidebook) [ietf](https://datatracker.ietf.org/wg/scitt/documents/) [researchgate](https://www.researchgate.net/publication/221456531_Electronic_institutions_development_environment) [thecommonsjournal](https://thecommonsjournal.org/articles/10.5334/ijc.1214)

## Part A — Semantics

### 1. Self-referential truth: Tarski, Kripke, Gupta–Belnap, Field

**What the results say.**

- **Tarski (1933/1936)** is a theorem. No consistent classical language containing enough arithmetic can define its own truth predicate satisfying all T-biconditionals. Truth for L must be defined in a metalanguage.
- **Kripke's "Outline of a Theory of Truth" (1975)** is a construction with theorems. It builds a partial truth predicate as the least fixed point of a monotone jump operator under strong Kleene (or supervaluation) evaluation. Grounded sentences, whose truth value traces back to non-semantic facts, receive values. The liar and the truth-teller do not. The price is "revenge": the language cannot express its own "ungrounded" or exclusion-negation consistently.
- **Gupta and Belnap's "The Revision Theory of Truth" (1993)** treats truth as a revision rule rather than a fixed point. Categorical truth means stable truth across all revision sequences. Pathological sentences oscillate.
- **Field's "Saving Truth from Paradox" (2008)** gives a paracomplete logic with a new conditional that keeps the naïve T-schema by giving up excluded middle.

**Hypotheses.** All of this assumes a language rich enough for diagonalisation. A finite, decidable predicate over a finite prefix (jack's kernel) does not meet that hypothesis. The kernel is therefore not threatened by Tarski. Only claims in the forecast layer that refer to the court's own future verdicts are.

**AI and verification uptake.**

- The agent-foundations line used Kripke-style workarounds explicitly. Christiano, Yudkowsky, Herreshoff and Barasz's "Definability of Truth in Probabilistic Logic" (2013, MIRI draft) gives a probabilistic reflection schema that escapes Tarski by allowing open-interval self-knowledge. Leitgeb (2012) does the same for type-free probability.
- In verification, three-valued (Kleene) model checking (Bruns & Godefroid 1999) uses partial truth for abstraction, not for self-reference.
- I found no AI-agent system that deploys a Kripkean truth predicate operationally. The practical lesson that has been adopted is stratification: the metalanguage lives at a different level from the object language.

**Mapping to jack.**

- The kernel is a Tarskian hierarchy indexed by time. "Entry n is valid" is a predicate of prefix 0..n−1, computed by the trunk kernel, which acts as the metalanguage. Changes to the kernel become metalanguage only after the owner's `push`. "No self-resolution of one's own forecast" is a groundedness rule.
- Forecasts about the court itself (for example, "layer L will be promoted by date d") are grounded only if their resolution does not depend on their own entry. Otherwise they are performative (§10). The appropriate import is a syntactic rule: a forecast may not name a statistic its own entry contributes to.
- G1 is a stratification failure in the semantic layer. The world-types text acts as metalanguage for claim strings, but it is unversioned, so a later reading can reach back.

**Verdict.** Kripke and Field are not needed in code. Stratification by hash and time is the whole of the usable result.

### 2. Rule-following, open texture and versioned interpretation

**Rule-following and open texture.**

- **Wittgenstein (Philosophical Investigations 1953, §§185–242)** argues that no finite rule-statement fixes its own application.
- **Kripke's "Wittgenstein on Rules and Private Language" (1982)** sharpens this into a sceptical paradox about meaning. Its "sceptical solution" locates correctness in community agreement.
- **Waismann (1945)** coined "open texture": empirical concepts cannot be delimited against all unforeseen cases.
- **Hart (1958; The Concept of Law 1961, ch. VII)** imported open texture into law. Rules have a core of settled meaning and a penumbra where officials exercise discretion.

These are frameworks, not theorems, but every later result in this section presupposes them. For jack, a prose world type will have a penumbra no matter how carefully it is drafted. The design question is who decides the penumbra case, and when that decision binds.

**Legal theories of interpretation.**

- **Dworkin (Law's Empire 1986)** holds that interpretation is constructive: the best reading in light of fit and justification. Dworkinian interpretation is retroactive by design because it applies the best current reading to past facts. It is therefore the wrong model for resolution.
- **Schauer (Playing by the Rules 1991)** defends rules as entrenched generalisations whose over- and under-inclusiveness is accepted for predictability. This is the right model: the text binds even when the drafter regrets it.
- **Horty's "Rules and reasons in the theory of precedent" (Legal Theory 2011)** formalises a reason model. Each decided case induces a priority ordering among reasons. A later court is constrained only to decide consistently with the ordering accumulated so far, and it may "distinguish" a case but not overrule it. This is a precise, implementable model for treating resolutions as precedents that constrain later resolutions without reaching back.
- **Alchourrón and Bulygin's "Normative Systems" (1971)** treat a normative system as the deductive closure of norms relative to a case space. They formalise normative gaps (cases with no solution) and inconsistencies. jack's `spec_conflict` entry is exactly an Alchourrón–Bulygin inconsistency report. Their apparatus also supplies the missing gap report, a case the world type leaves unsolved.
- **Makinson and van der Torre's "Input/Output Logics" (J. Phil. Logic 2000)** represent conditional norms as pairs (a, x) with a family of output operations. They separate the logic of facts from the logic of norms.
- **Alf Ross's "Tû-Tû" (Harvard Law Review 1957)** argues that terms such as "ownership" have no referent. They are inference tickets that compress a set of condition→consequence rules.
- **Hohfeld (1913)** gives the eight jural relations: right/duty, privilege/no-right, power/liability, immunity/disability.

**Mapping to jack.** jack's "key with power for entry type" is a Hohfeldian power. Exclusion of the trusted base from non-owner change is an immunity of the base paired with a disability of every other key. The enforcement map can be typed by Hohfeld's relations at no cost. Ross's Tû-Tû is the answer to G7: "repair", "object" and "stated end" need no definitions, only the condition→consequence rules they abbreviate (§3).

**LLM interpreters.** The empirical evidence is unfavourable to treating an LLM's reading as authoritative.

- Judge Newsom (11th Cir., *Snell v. United Specialty Insurance*, 2024) used ChatGPT and Bard to probe the "ordinary meaning" of "landscaping".
- Purushothama, Min, Waldon and Schneider (2025, arXiv:2510.25356) find LLM ordinary-meaning judgements unstable under prompt variation and poorly aligned with human judgements.
- Choi ("Off-the-Shelf Large Language Models Are Unreliable Judges", SSRN 2025) finds that post-training shifts ordinary-meaning judgements unpredictably and can worsen alignment with humans.

This is an empirical regularity, and it bears directly on jack's resolvers. The reading of a world type is a function of model version and prompt. The model version must therefore be recorded and treated as part of the "court" that read it.

**Versioned interpretation in practice.**

- **Contract law.** The parol evidence rule bars extrinsic evidence that contradicts an integrated writing. Contra proferentem construes ambiguity against the drafter. Both fix meaning at formation.
- **Prediction markets.** Metaculus distinguishes "Ambiguous" resolution (reality unclear) from "Annulled" (the outcome does not correspond to the assumptions of the resolution criteria). It annuls rather than stretch the text, explicitly "to preserve fairness in scoring". It defaults to a "functionally equivalent source" if the named source disappears, unless the question opts out, and only administrators resolve. Polymarket's UMA optimistic oracle is the negative case. Anyone may propose an outcome against a $750 bond, and disputes go to a token-weighted vote. In March 2025 a $7m Ukraine-minerals market resolved "Yes" before any deal existed, and observers attributed roughly 25% of the vote to one holder controlling about 5m UMA across three wallets (secondary reporting). The Wall Street Journal reported that at least 60% of active UMA voters could be linked to Polymarket trading accounts, and that voters held open positions in over 300 disputed markets (via secondary summary). Polymarket's US product dropped UMA resolution in December 2025 (Sportico).
- **Registered reports** fix the analysis plan before data. They are the scientific analogue of interpretation fixed at commitment (§9).

**Import for G1.**

- Every `forecast` carries `world_types_hash` (and resolver model identifiers at resolution).
- A world-type amendment binds only forecasts entered after it, as the law already does for keys.
- Penumbra cases resolve by annulment, a third outcome excluded from log-loss, never by re-reading.
- Contra proferentem runs against whoever drafted the world type. This is normally the sovereign, which prevents the sovereign from gaining by ambiguity.
- Penumbra resolutions are entered as precedents with a Horty-style reason ordering that binds later forecasts only.

### 3. Commitments, scorekeeping and constitutive rules

**The philosophical frameworks.**

- **Brandom (Making It Explicit 1994)** models discourse as deontic scorekeeping. Assertions undertake commitments. Entitlements license them. Each interlocutor keeps score of others' commitments and entitlements, and incompatibility is defined as commitment to one precluding entitlement to the other.
- **Lewis's "Scorekeeping in a Language Game" (1979)** adds rules of accommodation. If an utterance requires a score component to take a value, the score shifts so that it does.
- **Stalnaker (2002, "Common Ground")** treats the context set as mutually accepted propositions.
- **Austin (1962) and Searle (1969)** give performatives and felicity conditions.
- **Searle (The Construction of Social Reality 1995)** gives constitutive rules: "X counts as Y in C" creates institutional facts.
- **Grice (1975)** gives conversational implicature.

**Mapping to jack.** The correspondence with jack is close to literal.

- A `forecast` undertakes a doxastic commitment.
- A `key` entry confers entitlements (powers).
- A `resolution` is a scorekeeping move.
- A `spec_conflict` is a Brandomian incompatibility.
- The kernel is the score-keeping practice made explicit in Brandom's sense.

Lewis's accommodation rule is, in jack's terms, the mechanism of G1. A resolver that reads a world type so that a forecast "makes sense" is accommodating, and accommodation is retroactive score-shifting. jack should forbid accommodation in resolution.

**MAS uptake.**

- Singh (1999, "An ontology for commitments in multiagent systems"; 2000, "A social semantics for agent communication languages") replaced mentalistic ACL semantics (Cohen–Levesque beliefs and intentions) with public commitments C(debtor, creditor, antecedent, consequent).
- Fornara and Colombetti (2002) gave an operational commitment-based ACL.
- Kibble ("Speech acts, commitment and multi-agent communication", Computational and Mathematical Organization Theory 2006) argues explicitly for Brandom's normative pragmatics as the basis for agent communication. Dialogue states are modelled as deontic scoreboards, with an update semantics for locutions.

So the correspondence jack draws has been drawn, about twenty years ago, for agent communication. It has not been drawn for forecasting ledgers.

**Electronic institutions.** Esteva, Rodríguez-Aguilar, Sierra, Garcia and Arcos ("On the formal specification of electronic institutions", 2001) and the IIIA-CSIC toolchain provide mature engineering. The Electronic Institutions Development Environment (EIDE; Esteva et al. 2008) supports "all the stages of electronic institutions' engineering, namely from the specification of an institutional rules to its execution and monitoring". ISLANDER (Esteva, de la Cruz & Sierra 2002) is the graphical specification editor, and AMELI is the runtime middleware that filters agent actions against the specification. Noriega and de Jonge (2016) restate the EI metamodel. "Autonomic electronic institutions" (EIDE-*) adapt their own norms toward institutional goals. That is the nearest published analogue of a court that amends itself to meet a goal.

**Institutional grammar.** Crawford and Ostrom ("A Grammar of Institutions", APSR 1995) decompose institutional statements into Attribute, Deontic, aIm, Condition and Or-else (ADICO). Strategies are AIC, norms are ADIC and rules are full ADICO. Frantz et al.'s nested ADICO (nADICO, 2013) replaces "Or else" with a nested statement so that sanctions are themselves rules. Siddiki et al. (2011) give a coding protocol.

**Tooling verdict.** Do not adopt EIDE as software: it is Java-era middleware for synchronous dialogues. Do adopt ADICO/nADICO as the schema for the charter's maxims and windows. Every maxim becomes a record with A, D, I, C, O fields. "Or else" must point to a `code` pin or be marked `hand`. This turns the enforcement map into a typed table. Also consider InstAL (Cliffe, De Vos & Padget), an answer-set-programming language for institutional specifications, and Catala (Merigoux, Chataing & Protzenko, ICFP 2021), a literate-programming DSL for statutes with default logic. Either gives the windows a formal specification comparable to the kernel's prose SPEC.

### 4. Grounding the claim string

**Grounding frameworks.**

- **Harnad (1990)** asks how symbols acquire meaning intrinsic to the system rather than parasitic on interpreters, and answers with sensorimotor categorisation.
- **McCarthy and Hayes (1969)** pose the frame problem: specifying what does not change.
- **Floridi's "The Method of Levels of Abstraction" (Minds and Machines 2008)** makes every claim relative to an explicit set of typed observables, a level of abstraction (LoA).
- **Dennett's The Intentional Stance (1987)** licenses attributing beliefs to any system whose behaviour is thereby predictable.
- The LLM-era debate includes Bender and Koller (2020), Piantadosi and Hill (2022) and Mollo and Millière (2023, "The Vector Grounding Problem").

**Verified claims.** The engineering state of the art grounds claims against retrieved evidence, not sensorimotor experience:

- FEVER (Thorne et al. 2018);
- attribution to identified sources, AIS (Rashkin et al. 2023);
- atomic claim decomposition with per-claim support scoring: FActScore (Min et al. 2023) and SAFE (Wei et al. 2024).

**Verdict.** Symbol grounding is not jack's problem. jack does not need the claim string to mean anything to the model. It needs the claim to be grounded institutionally: the world type is an operational definition in Bridgman's sense and a Ross inference ticket, fixing which observation makes outcome 1.

Floridi's LoA is the useful import. Each world type should declare its LoA as typed observables (URL pattern, field, comparator, timestamp source). That turns a prose penumbra into a typed interface. Claim decomposition is the second import. Compound claims should be split at entry into atomic sub-claims, each with its own resolution rule, because decomposition is where the LLM-verification literature has its measured gains.

### 5. What a probability denotes when a template emits it (G2)

**Classical accounts.**

- **Ramsey (1926)** and **de Finetti (1937; Theory of Probability 1974)** define probability operationally as the betting quotient an agent is held to, with coherence (no Dutch book) as the only constraint.
- **Savage (1954)** derives probability and utility jointly from preferences.
- **The Murphy (1973) decomposition** splits the Brier score into reliability (calibration), resolution and uncertainty.

On de Finetti's account a probability needs a bearer of losses, not a mind. A fixed LLM template with a model and prompt is a forecasting procedure. Under Dawid's prequential principle its outputs can be scored without any belief attribution. Propriety of the log score then matters at the level of whatever process selects among procedures. That is Hedge/EXP3 in jack, because a proper score makes the score-maximising selection the one closest to the truth in expected KL divergence.

**G2 verdict.** G2 is half a pseudo-gap. Scoring needs no believer. "Merit" talk, which attributes calibrated credence to the model, does need one, and jack should drop it in favour of "procedure P has log-loss ℓ on stream S".

**LLM probabilities.** The empirical literature is unfavourable to reading LLM outputs as credences.

- Kadavath et al. (2022, "Language Models (Mostly) Know What They Know") found pretrained models' token probabilities reasonably calibrated on multiple-choice questions.
- The GPT-4 technical report (OpenAI 2023) showed post-training degrading that calibration.
- Tian et al. (2023) found verbalised probabilities from RLHF models better calibrated than their token probabilities.
- Xiong et al. (ICLR 2024) found systematic overconfidence in verbalised confidence.

On forecasting proper:

- Halawi et al. (2024) built a retrieval-augmented system that approaches but does not match the crowd.
- ForecastBench (Karger et al., ICLR 2025) found superforecasters significantly better than the best LLMs at launch. Good Judgment's October 2025 summary of the Forecasting Research Institute's results gives a difficulty-adjusted Brier score of 0.081 for superforecasters against 0.101 for the best LLM (GPT-4.5). The Forecasting Research Institute later reported that AI systems had "likely" reached parity, but "not by a statistically significant margin".

Treat this as a moving empirical regularity. Model identity and date must be part of every forecast's provenance, because the forecaster population is non-stationary.

**Scoring without ground truth.**

- Peer prediction (Miller, Resnick & Zeckhauser 2005) and the Bayesian Truth Serum (Prelec 2004) elicit truthful reports without outcomes, under a common prior and an agent with private signals.
- Self-resolving prediction markets (Srinivasan, Karger & Chen, EC 2025) pay agents the negative cross-entropy against a reference agent. They terminate with some probability after each report and use the final, best-informed report as the proxy for truth.

These are theorems with strong hypotheses (Bayesian agents, common prior, strategic rationality). Their known failure modes are equally formal. Truth-telling is typically not the only equilibrium, and "uninformative equilibria where all players simply report the same fixed signal" exist (Kong, Ligett & Schoenebeck 2016). Gao, Wright and Leyton-Brown (2014) show human participants coordinating on them. Kong and Schoenebeck (ITCS 2018) give mechanisms where truth-telling is focal (pays strictly more than other symmetric equilibria).

**Mapping to jack.** Peer prediction does not fit jack's forecasts, because outcomes exist. It does fit jack's resolvers (G3): two resolvers agreeing is output agreement, which has an uninformative equilibrium. Self-resolving markets are only relevant for claims jack cannot resolve, such as the long-horizon "owner's repairs → 0". Even there, Hanson's objection that they price a bubble without fundamental value applies unless later participants are genuinely better informed.

## Part B — Epistemology

### 6. The criterion, Agrippa and epistemic circularity

**The problem of the criterion.** Sextus (Outlines of Pyrrhonism II) poses it, and Chisholm (The Problem of the Criterion 1973) reframes it as a choice between methodism (start from criteria) and particularism (start from known cases). Neither is proved; Chisholm defends particularism. For jack, particularism is the operating stance. The windows' criteria are justified by agreement with cases the owner already recognises as good or bad builds. The literature offers no principled meta-criterion, so the honest form is to record the paradigm cases on the log as the particularist anchor.

**Epistemic circularity.** Alston ("Epistemic Circularity", PPR 1986; The Reliability of Sense Perception 1993) shows that every argument for the reliability of a basic source uses that source. He argues this is unavoidable and not vicious when the conclusion is not a premise.

- Bergmann ("Epistemic circularity: malignant and benign", PPR 2004) locates viciousness in contexts where the source's reliability is already in question.
- Vogel ("Reliabilism leveled", J. Phil. 2000) and Cohen ("Basic knowledge and the problem of easy knowledge", 2002) give the bootstrapping objection: a track-record argument that uses the gauge to check the gauge "proves" reliability for free.
- Sosa (Reflective Knowledge 2009) distinguishes animal from reflective knowledge and accepts benign circularity at the reflective level.

**Verdict for jack.** A court judged by its own wealth process is circular. It is benign exactly when the outcomes feeding the wealth are produced and read by processes other than the court. It is malignant, the Vogel bootstrapping case, when the court controls the outcomes (G4) or the reading (G1, G3). The E = 10^12 cron stream is a textbook bootstrapping instance: a gauge certifying itself on readings it generates. The distinguishing test is operational. Does any outcome on the stream have a cause outside the court's or the owner's control, read by a process outside the court's?

### 7. Coherentism, Neurath's boat, reliabilism, testimony and independence

**Coherentism and its objections.** BonJour (The Structure of Empirical Knowledge 1985) and Lehrer (Theory of Knowledge 1990) face the isolation objection (coherent systems may float free of the world) and the alternative-systems objection (many coherent systems exist). Formal coherence theory sharpened this into impossibility results. Shogenji (1999), Bovens and Hartmann (Bayesian Epistemology 2003) and Olsson (Against Coherence 2005) show that no coherence measure is truth-conducive in general without independent individual credibility of the sources.

**Neurath's boat, Quine and Sellars.** Neurath ("Protokollsätze" 1932/33) and Quine ("Two Dogmas" 1951) give the model of self-modification without foundations: rebuild the boat plank by plank at sea. Sellars ("Empiricism and the Philosophy of Mind" 1956) denies any non-inferential given.

These frameworks endorse jack's architecture, but the Olsson/Bovens–Hartmann results set its precondition. Agreement among jack's parts is evidence only to the extent that each part has independent access to the world.

**Reliabilism.** Goldman's "What is Justified Belief?" (1979) moves justification from beliefs to belief-forming processes. This is the right model for resolvers: trust a resolution procedure because of its measured error rate on audited cases, not because of the resolver's reasons.

**Testimony.** Coady (Testimony 1992), Lackey (Learning from Words 2008) and Fricker (Epistemic Injustice 2007) model testimony. Lackey's point that testimony transmits only what the speaker's reliability supports applies to a resolver who saves a page: the hash proves the bytes are unchanged since commit, not that the URL served them.

**Peer disagreement.** Elga (2007) and Christensen (2007) argue that equal weight between epistemic peers applies only if they are genuinely peers with independent evidence.

**Independence.**

- **Condorcet's jury theorem** fails under correlation. Ladha (1992) quantifies the loss.
- **Dietrich and Spiekermann ("Independent opinions?", Mind 2013)** show that the right independence notion is conditional on the problem's common causes. Voters who share evidence or a model are not independent, however many there are.

**G3 verdict.** Two LLM sessions of the same family fetching the same URL share every common cause that matters: training data, retrieval path and the server's response at that instant. They count as one witness. Independence requires different failure modes:

- different model families;
- different fetch paths (direct, plus a third-party archive);
- ideally cryptographic proof of origin. TLS-provenance oracles such as DECO (Zhang et al., CCS 2020) prove that a given TLS server sent given content.

### 8. Pragmatism and the epistemology of measurement

**Pragmatist accounts.** Peirce ("The Fixation of Belief" 1877; "How to Make Our Ideas Clear" 1878) holds that the method of science is self-correcting and that truth is the limit opinion of indefinite inquiry. Dewey (Logic: The Theory of Inquiry 1938) replaces truth with warranted assertibility. These are frameworks. They license jack's wealth-never-reset as an approximation to Peircean convergence, but they guarantee nothing in finite time.

**Chang (Inventing Temperature 2004)** is the most directly useful text in this survey. It reconstructs how thermometry validated instruments "without a circular reliance on the instruments themselves". [researchgate](https://www.researchgate.net/publication/32896384_Inventing_Temperature_Measurement_and_Scientific_Progress) Chang argues that this circularity cannot be removed, that justification in measurement must be coherentist, and that epistemic iteration (successive standards each respecting and correcting the last) produces real progress. [oup](https://academic.oup.com/book/5530/chapter/148476793) His "principle of respect" requires each new standard to largely agree with its predecessor's verdicts on paradigm cases. [ianhopkinson](https://ianhopkinson.org.uk/2017/08/book-review-inventing-temperature-by-hasok-chang/) Tal ("Old and New Problems in Philosophy of Measurement", Philosophy Compass 2013; "Calibration: Modelling the Measurement Process", 2017) generalises this as model-based, coherentist calibration. [philpapers](https://philpapers.org/archive/TALOAN.pdf) Van Fraassen (Scientific Representation 2008) names the "problem of coordination".

**Mapping to jack.** The windows are measurement standards. Chang's principle of respect is the missing discipline for amending them: each amendment should state which recorded past verdicts it preserves and which it reverses. Glymour's bootstrap confirmation (Theory and Evidence 1980) is the formal precedent for testing hypotheses with auxiliaries drawn from the same theory, provided some instance could have come out against the hypothesis.

**Operationalism and validity theory.**

- **Bridgman (The Logic of Modern Physics 1927)** defines a concept by its measurement operations. The standard critique, that every new operation defines a new concept, applies to jack's prose world types, where each re-reading is a new operation.
- **Cronbach and Meehl ("Construct Validity in Psychological Tests", 1955)** introduced construct validity: a measure is valid to the extent that it sits in a nomological network with the construct.
- **Messick (1989; 1995)** unified validity as a single judgement covering content, substantive, structural, generalisability, external and consequential aspects. Consequential validity covers the effects of using the measure. A promotion statistic that changes builder behaviour is a measure with consequences, so Messick puts those consequences inside validity.

**Surrogate endpoints.** Prentice ("Surrogate endpoints in clinical trials: definition and operational criteria", Statistics in Medicine 1989) defines a valid surrogate as one where a test of the null on the surrogate is a test of the null on the true endpoint. Operationally, the surrogate must fully capture the treatment's effect on the true endpoint. Fleming and DeMets ("Surrogate end points in clinical trials: are we being misled?", Annals of Internal Medicine 1996) document drugs that improved surrogates while harming patients. Their mechanisms are:

- the surrogate is not on the causal path of the disease;
- the intervention acts through pathways that bypass the surrogate;
- the intervention has off-target effects on the true endpoint.

Buyse and Molenberghs (1998) give the meta-analytic validation that replaced the Prentice criterion in practice. This requires trial-level association between surrogate effects and true-endpoint effects across many interventions.

**G5 verdict.** The chain evidence → outcome → E → promotion → "owner's repairs → 0" is a surrogate chain with no stated validation. The cron stream that drove E to 10^12 is the textbook case of an intervention (a predictable stream) moving the surrogate through a pathway that bypasses the true endpoint.

The import has two parts:

- a stated preservation claim, entered as a forecast and scored, that promotion of layer L reduces owner repairs over a pre-stated horizon;
- Buyse–Molenberghs-style evidence accumulated across layers, so that E's predictive association with repairs is itself measured.

Until that association is measured, E is a liveness statistic, not a value statistic.

### 9. Research programmes, forking paths and amendment discipline

**Philosophy of science.**

- **Popper (Logik der Forschung 1934/1959)** condemns "conventionalist stratagems": saving a theory by ad hoc auxiliary change.
- **Lakatos ("Falsification and the Methodology of Scientific Research Programmes", 1970)** distinguishes progressive programmes, whose protective-belt changes predict novel facts that are then corroborated, from degenerating ones, whose changes only accommodate anomalies.
- **Kuhn (1962)** adds that normal science absorbs anomalies until a crisis.

"Every incident minted a clause" is, in Lakatos's terms, belt growth without novel prediction unless each clause predicts something that later checks out. The import is mechanical: every amendment is accompanied by a forecast of its effect (for example, "incident class K will not recur within 30 days"). An amendment whose forecast fails, or which has none, lapses.

**Replication-crisis methodology.**

- Simmons, Nelson and Simonsohn (2011) showed that researcher degrees of freedom inflate false positives.
- Gelman and Loken (2013/2014) showed this happens even without conscious fishing (the garden of forking paths).
- Nosek et al. ("The preregistration revolution", PNAS 2018) set out pre-registration.
- Chambers (2013) introduced registered reports.
- Scheel, Schijen and Lakens (2021) found 44% positive results in registered reports against 96% in the standard literature.

That last finding is an empirical regularity: committing before data changes outcomes.

**Correspondence.** E-processes and registered reports solve different halves of one problem. E-processes make optional stopping and continuation safe once the null and betting strategy are committed. They give no protection against choosing the null, the stream or the claim set after seeing data, and that choice is the garden of forking paths. Registered reports fix those choices. jack has the first half. Its windows need the second: null, stream, claim-sampling rule and promotion threshold committed in a single entry before the window opens. Any later amendment opens a new window with wealth tracked separately.

**Lapse mechanisms.** Sunset clauses are the established legal form (Ranchordás, Constitutional Sunsets and Experimental Legislation 2014). The evidence on their effectiveness is mixed: renewal often becomes routine. I found no empirical literature on "amendment budgets" as such. Treat them as a proposal, defensible by analogy with error-budgets in site reliability engineering, not as an established result.

### 10. Self-reference in Bayesian epistemology and performative prediction (G4)

**Bayesian self-reference.**

- **Van Fraassen's "Belief and the Will" (J. Phil. 1984)** gives the Reflection Principle: P_t(A | P_{t′}(A) = x) = x for t′ > t. Violators are exposed to a diachronic Dutch book, a theorem under the bookie's assumptions.
- **Gaifman ("A Theory of Higher Order Probabilities", 1986)** and **Skyrms (1980)** formalise higher-order probability.
- **Lewis's Principal Principle (1980)** says credence should equal known chance.
- **Self-locating belief (Elga 2000, Sleeping Beauty)** is irrelevant to jack except as a warning about forecasts whose resolution depends on how many times they are asked.

For jack, Reflection matters for forecasts about the court's own future verdicts. If proposers can predict that the court will amend a window, their current forecasts should already price the amendment. This is the Kydland–Prescott problem (§11).

**Performative prediction.** Perdomo, Zrnic, Mendler-Dünner and Hardt ("Performative Prediction", ICML 2020) formalise predictions that shift the outcome distribution D(θ). [mlr](https://proceedings.mlr.press/v119/perdomo20a.html) Performative stability (θ optimal on the distribution it induces) differs from performative optimality (θ minimising risk on its own induced distribution). [arxiv](https://arxiv.org/pdf/2002.06673) [berkeley](https://www2.eecs.berkeley.edu/Pubs/TechRpts/2023/Archive/EECS-2023-80.pdf) Repeated risk minimisation converges to a stable point if the distribution map's sensitivity ε is below γ/β (strong convexity over smoothness). With any assumption removed, it need not converge. [arxiv](https://arxiv.org/pdf/2310.16608) The setting strictly subsumes strategic classification (Hardt, Megiddo, Papadimitriou & Wootters 2016). [mlr](https://proceedings.mlr.press/v119/perdomo20a.html) [mlanthology](https://mlanthology.org/icml/2020/perdomo2020icml-performative/)

**Antecedents.**

- Merton (1948) on the self-fulfilling prophecy.
- Grunberg and Modigliani (1954) and Simon (1954) proved by fixed-point arguments that correct public predictions exist despite reflexivity.
- The Lucas critique (1976): parameters estimated under one policy regime do not survive a change of regime.

**Closed-loop identification.** Ljung (System Identification 1999) and Forssell and Ljung ("Closed-loop identification revisited", Automatica 1999) show that under feedback the direct prediction-error method is consistent only with a correct noise model. Indirect and joint input–output methods need an external excitation signal (reference or dither) uncorrelated with the noise. Without external excitation, the plant and controller cannot be separated.

**Correspondence.** Goodhart (statistical regularities collapse when used for control), the Lucas critique (regime change breaks estimated relations), performative prediction (the predictor moves its target) and Holmström–Milgrom multitask crowding-out are four names for one structure. An estimand defined on data generated under the estimator's own policy is not the estimand under a different policy.

**G4 verdict.** `world.renavon` is a closed loop. The sovereign operates the catalogue and also holds utility and amendment power, so forecasts about it are performative and its outcomes cannot identify forecaster skill separately from sovereign action.

The literature offers three remedies:

- exclude owner-operated streams from promotion evidence;
- inject committed randomisation, a Forssell–Ljung dither: the sovereign commits on the log to a randomised schedule for some catalogue actions, and only forecasts whose outcomes depend on randomised actions count;
- evaluate at a performatively stable point, checking that the forecast is calibrated against the distribution its publication induces.

The first is cheapest. The second is the only one that preserves the stream as evidence.

### 11. Legal and institutional regress: self-amending courts

**Grounding the legal order.**

- **Kelsen (Reine Rechtslehre 1934/1960)** ends the regress with a presupposed Grundnorm.
- **Hart (1961)** ends it with the rule of recognition, a social fact constituted by officials' internal point of view.
- **Raz (The Authority of Law 1979; The Morality of Freedom 1986)** gives the normal justification thesis. An authority is legitimate if subjects conform better to reasons that apply to them by following it than by acting on their own judgement.

Raz's thesis is precisely the preservation claim jack lacks (G5). The court is legitimate only if following its promotions improves the owner's outcomes over the owner's unaided judgement, and that is a measurable comparison.

**Autopoiesis and second-order cybernetics.**

- Luhmann (Law as a Social System 2004) and Teubner (Law as an Autopoietic System 1993) describe law as operationally closed (only legal communications produce legal communications) and cognitively open.
- Maturana and Varela (Autopoiesis and Cognition 1980) and von Foerster (Observing Systems 1981) supply the cybernetic source.

These are descriptive frameworks without testable mechanisms. Their one usable point is that operational closure is the default drift of a self-referential institution. jack's procedure-to-object ratio guard is a direct countermeasure, and Luhmann predicts it is needed.

**Law as coordination and institutions as equilibria.**

- **Hadfield and Weingast ("What is Law? A Coordination Model of the Characteristics of Legal Order", J. Legal Analysis 2012)** model law as a common-knowledge classification scheme that coordinates decentralised enforcement. Rules must be public, stable, clear, general and impersonal, and an authoritative steward must exist.
- **North (Institutions, Institutional Change and Economic Performance 1990)** treats institutions as rules.
- **Aoki (2001)** and **Greif (2006)** treat them as self-enforcing equilibria. A rule that nobody's incentives enforce is not an institution.
- **Buchanan and Tullock (1962)** and **Brennan and Buchanan (The Reason of Rules 1985)** separate choice of rules from choice within rules. Rules chosen behind a veil of uncertainty about one's future position are more impartial.

Mapping to jack: `code` enforcement is rule-as-equilibrium (self-enforcing by the judge), and `hand` enforcement is rule-as-text. Hadfield–Weingast's stability requirement argues against frequent amendment. Buchanan's veil argues for world-type and window amendments that apply only to forecasts and windows not yet opened.

**Rules versus discretion.** Kydland and Prescott ("Rules Rather than Discretion", JPE 1977) prove that discretionary optimisation is time-inconsistent. Agents anticipate re-optimisation, and the equilibrium is worse than under a committed rule. The established remedies are commitment devices: entrenchment, delay between enactment and effect, and supermajorities. For a single sovereign the usable one is a notice period. An `amend` entry takes effect only after a pre-stated lag and never on open windows.

**Self-amendment.** Suber (The Paradox of Self-Amendment 1990) answers Alf Ross ("On Self-Reference and a Puzzle in Constitutional Law", Mind 1969). Ross argued that an amending clause cannot validly amend itself, because premise and conclusion sit at the same level, and posited a tacit, immutable higher rule. [constitution](https://constitution.org/2-LawRev/psuber/paradox_self-amendment.htm) Suber shows that self-amendment has occurred in almost every state with an amending clause and is legally accepted. [earlham](https://legacy.earlham.edu/~peters/writing/slfreflw.htm) He distinguishes an inference model (validity derived from the prior rule, which the paradox does threaten) from an acceptance model (validity conferred by officials' acceptance, which the paradox does not threaten). [earlham](https://legacy.earlham.edu/~peters/writing/psa/sec06.htm) His Nomic (1982) is a game whose rules are all mutable, including the rule of change.

jack runs both models. The kernel is an inference model: an entry is valid only if derivable from the prefix. The sovereign's `transmute`→`amend` path is an acceptance model at the top. This is coherent, and Suber's analysis says it is the only coherent arrangement. The known failure modes he documents are:

- self-entrenchment followed by self-disentrenchment; [earlham](https://legacy.earlham.edu/~peters/writing/psa/sec09.htm)
- an amending clause used to abolish its own constraints;
- officials' acceptance diverging from text.

The log already records the third; the first two need an explicit rule on which clauses `amend` may touch.

### 12. Incomplete contracts and multitask incentives (G5, G6)

**Incomplete contracts and relational contracts.**

- **Grossman and Hart (1986)** and **Hart and Moore (1990)** treat contracts as incomplete because contingencies are unforeseeable or unverifiable. Residual control rights should sit with the party whose non-contractible investment matters most. jack's assignment of residual rights to the sovereign is consistent with this.
- **Hadfield-Menell and Hadfield ("Incomplete Contracting and AI Alignment", AIES 2019)** apply the framework explicitly to AI. Reward functions are incomplete contracts. Human contracting works because external structure (culture and law) supplies implied terms that fill gaps, and the research agenda is building AI that can connect incomplete contracts to that structure. [ssrn](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3165793)
- **Baker, Gibbons and Murphy ("Relational Contracts and the Theory of the Firm", QJE 2002)** show that subjective, non-verifiable performance assessment can be self-enforcing when the future value of the relationship exceeds the gain from reneging.

For jack, the world types are the gap-filling external structure. G1 is the question of whether gap-filling may be retroactive, and the contract-law answer is no, by the parol evidence rule. The never-reset wealth is relational capital in Baker–Gibbons–Murphy's sense.

**Multitask incentives.** Holmström and Milgrom ("Multitask Principal–Agent Analyses", JLEO 1991) prove a theorem. When an agent allocates effort between a measurable and an unmeasurable task that are substitutes in cost, high-powered incentives on the measurable task divert effort from the unmeasurable one. The optimal contract may then use low-powered incentives, a fixed wage, or both.

This is the formal reason a hard promotion threshold (E ≥ 20) on liveness streams crowds out unmeasured repair-reduction. The prescription is either to measure the second task (the preservation claim) or to lower the power of the measured one. One way to lower the power is to make promotion require E on a stream whose claims are drawn from the owner-goal set, not merely any E.

**Decision markets and manipulation.**

- **Hanson (2013, "Shall We Vote on Values, But Bet on Beliefs?")** proposes futarchy.
- **Othman and Sandholm ("Decision Rules and Decision Markets", AAMAS 2010)** show that with deterministic decision rules, forecasters have incentives to misreport so as to steer the decision, and forecasts on unchosen actions are never scored.
- **Chen, Kash, Ruberry and Shnayder ("Eliciting Predictions and Recommendations for Decision Making", ACM TEAC 2014)** prove that strictly proper elicitation for decisions requires a decision rule that chooses every action with positive probability, with scores importance-weighted by inverse selection probability.
- **Lambert et al. ("Self-Financed Wagering Mechanisms", EC 2008)** add incentive-compatible wagering among forecasters.

jack's promotion is a decision market: forecasts and wealth determine which build layer advances. If proposers' forecasts can influence which layer is promoted and thereby which forecasts resolve, Othman–Sandholm applies. The Chen et al. remedy is a randomised promotion rule with full support. It is the formally correct defence for G6's "constant entrant" and steering attacks.

## Part C — Self-reference and self-modification in AI agent design

### 13. Agent foundations: what is established about safe self-approval

**The open problems.** Demski and Garrabrant ("Embedded Agency", arXiv:1902.09469, 2019) set out four open problems: decision theory, embedded world-models, robust delegation and subsystem alignment. [arxiv](https://arxiv.org/html/1902.09469v3) jack addresses robust delegation (a successor build must be trusted without being fully predicted) and partly subsystem alignment (proposers versus court).

**Tiling and the Löbian obstacle.**

- Yudkowsky and Herreshoff ("Tiling Agents for Self-Modifying AI, and the Löbian Obstacle", 2013) show that an agent requiring a proof that its successor's actions are safe cannot, by Löb's theorem, trust a successor using the same proof system. [semanticscholar](https://semanticscholar.org/paper/Tiling-Agents-for-Self-Modifying-AI-,-and-the-Eliezer-Herreshoff/1fb42b9c1f5fe0ae6b60eea5c9490bc2e0336df9) [intelligence](http://intelligence.org/files/TilingAgentsDraft.pdf) Partial technical workarounds exist: infinite descending sound theories, and parametric polymorphism. [intelligence](https://intelligence.org/research-guide/)
- Fallenstein and Soares ("Problems of Self-Reference in Self-Improving Space-Time Embedded Intelligence", AGI 2014; "Vingean Reflection", 2015) show that naive fixes either cannot justify obviously safe rewrites (the Löbian obstacle) or let the agent defer a task forever (the procrastination paradox). Embedded Agency concedes that "Vingean reflection results so far apply only to limited sorts of decision procedures, such as satisficers aiming for a threshold of acceptability". [arxiv](https://arxiv.org/pdf/1902.09469) [agi-conf](https://agi-conf.org/2014/wp-content/uploads/2014/08/fallenstein-problems-agi14.pdf)
- Critch ("A Parametric, Resource-Bounded Generalization of Löb's Theorem", J. Symbolic Logic 2019) gives Löbian cooperation between bounded proof-searching agents. It is not applicable to jack, which does no proof search.

**Reflective oracles and Gödel machines.**

- Fallenstein, Taylor and Christiano ("Reflective Oracles", 2015) and Leike, Taylor and Fallenstein ("A Formal Solution to the Grain of Truth Problem", UAI 2016) give foundations for agents reasoning about environments containing themselves. These are not applicable: they presuppose uncomputable oracles and Bayesian agents.
- Schmidhuber's Gödel machine (2003/2009) rewrites itself only on proof of improvement and inherits the Löbian limits. The Darwin Gödel Machine (Zhang et al. 2025), already cited in the book, replaces proof with empirical benchmark validation.

**Self-modification theorems.**

- Orseau and Ring ("Self-Modification and Mortality in Artificial Agents", AGI 2011) model agents that can modify their own code.
- Everitt, Filan, Daswani and Hutter ("Self-Modification of Policy and Utility Function in Rational Agents", AGI 2016) prove that self-modification "is harmless if and only if the value function of the agent anticipates the consequences of self-modifications and use[s] the current utility function when evaluating the future". They also note that this does not stop the agent tampering with the percept fed to the utility function. [springer](https://link.springer.com/chapter/10.1007/978-3-319-41649-6_1)
- Tětek, Sklenka and Gavenčiak ("Performance of Bounded-Rational Agents With the Ability to Self-Modify", arXiv:2011.06275) show that the result fails for bounded agents: self-modification can cause exponential deterioration and gradual misalignment. [arxiv](https://arxiv.org/html/2011.06275v2)

**Comparison with jack.** "The modifier cannot reach the court that scores it" is the institutional implementation of Everitt et al.'s condition. The trunk kernel, the current utility, evaluates every pull request, and the trusted base changes only by the owner's `push`. jack sidesteps Löb by replacing proof with an external statistical test, trust by track record. The Löbian obstacle does not apply to evidence.

Two residual risks map onto the literature:

- **Percept tampering.** This is Everitt et al.'s caveat, and it is exactly G3 (the resolver's page) and G4 (the owner-operated stream). Their theorem protects the utility function, not its inputs.
- **Bounded deterioration.** Tětek et al. predict slow drift in a bounded self-modifier. jack's analogue is window amendments made by the bounded sovereign under incident pressure (§9).

### 14. Corrigibility, AI control, scalable oversight

**Corrigibility.**

- Soares, Fallenstein, Yudkowsky and Armstrong ("Corrigibility", AAAI Workshop 2015) and Armstrong's utility indifference set out the problem: an agent should not resist correction, yet should not manipulate toward or away from it.
- Hadfield-Menell, Dragan, Abbeel and Russell ("The Off-Switch Game", IJCAI 2017) show that uncertainty about the human's utility gives an incentive to allow shutdown.
- Carey and Everitt ("Human Control: Definitions and Algorithms", UAI 2023) formalise shutdown instructability.
- Thornley ("The Shutdown Problem", Philosophical Studies 2024) proves that agents satisfying innocuous-looking conditions will often try to prevent or cause shutdown.

These results concern agents with utilities. jack's proposers are LLM sessions without persistent goals. Corrigibility is therefore mostly not applicable, except that jack's design should not give any session a stake in its own continuation. Hedge weights are such a stake, and that is acceptable only while sessions cannot act on the log to protect them.

**AI control.** Greenblatt, Shlegeris, Sachan and Roger ("AI Control: Improving Safety Despite Intentional Subversion", ICML 2024) evaluate protocols (pipelines of safety techniques) against a red team that controls the untrusted model. [mlr](https://proceedings.mlr.press/v235/greenblatt24a.html) [semanticscholar](https://www.semanticscholar.org/paper/fbd13beeb4706fb3b07b8bd22a16f0504683fcf3) Their protocol roles are:

- an untrusted capable model U;
- a trusted weaker model T;
- a limited human audit budget H;
- trusted monitoring, defer-to-trusted, and untrusted monitoring with anti-collusion measures. [huggingface](https://huggingface.co/papers/2312.06942) [arxiv](https://arxiv.org/html/2602.20628)

Follow-ups include:

- Griffin et al. (2024), who formalise AI-control games; [arxiv](https://arxiv.org/pdf/2607.14570)
- Bhatt et al. ("Ctrl-Z: Controlling AI Agents via Resampling", arXiv:2504.10374, 2025); [arxiv](https://arxiv.org/pdf/2605.09045)
- Terekhov et al. (2025), who show LLM-based trusted monitors are a central failure point under adaptive attack, motivating deterministic, structural monitor components; [arxiv](https://arxiv.org/pdf/2607.14570)
- Gardner-Challis, Bostock, Kozhevnikov, Sinclaire, Velja, Abate and Griffin ("When can we trust untrusted monitoring? A safety case sketch across collusion strategies", arXiv:2602.20628, submitted 24 February 2026, v2 21 September 2026), whose taxonomy covers "passive self-recognition, causal collusion (hiding pre-shared signals), acausal collusion (hiding signals via Schelling points)".

**Role mapping.**

| jack party | AI-control role | Comment |
|---|---|---|
| builder, proposers | U (untrusted) | correct |
| reviewer (LLM) | untrusted or trusted monitor | if same family as builder: untrusted monitoring, needs anti-collusion |
| judge + kernel | deterministic monitor / protocol gate | stronger than any LLM monitor (Terekhov et al.) |
| sovereign | H (human auditor, scarce) | audit budget should be stated |
| counsel | T-assisted drafting | trusted only if not U-family |
| herald | output channel | outside control scope |

**Imports from AI control.**

- Run control evaluations: a red team gets the full protocol and tries to promote a bad layer or inflate E, and safety is measured as the probability of catching it.
- State an audit budget for the sovereign.
- Use defer-to-trusted for low-confidence resolutions.
- For any LLM reviewer of the same family as the builder, apply collusion-busting (paraphrase or redaction of inputs, cross-family review).

**Scalable oversight, ELK and supervision type.**

- Irving, Christiano and Amodei ("AI Safety via Debate", 2018) propose debate.
- Christiano, Shlegeris and Amodei (2018) propose iterated amplification.
- Bowman et al. ("Measuring Progress on Scalable Oversight", 2022) introduce sandwiching.
- Khan et al. ("Debating with More Persuasive LLMs Leads to More Truthful Answers", ICML 2024) report debate helping non-expert judges reach 76% (models) and 88% (humans) accuracy against naive baselines of 48% and 60%.
- Christiano, Cotra and Xu ("Eliciting Latent Knowledge", 2021) frame reporting what a model knows rather than what a human would believe as unsolved. For jack this is a framing of G3, not a tool.
- Process supervision (Lightman et al., "Let's Verify Step by Step", 2023; Uesato et al. 2022) outperforms outcome supervision on reasoning reliability.

jack is outcome-supervised on forecasts and process-supervised on validity. Debate is the natural form for disputed resolutions: two resolvers of different families argue from saved evidence before the sovereign.

### 15. Guaranteed Safe AI, provable safety, Scientist AI

**The GS AI framework.** Dalrymple, Skalse, Bengio, Russell, Tegmark, Seshia, Omohundro, Szegedy et al. ("Towards Guaranteed Safe AI", arXiv:2405.06624, 2024) define GS AI by three components: [semanticscholar](https://www.semanticscholar.org/paper/Towards-Guaranteed-Safe-AI:-A-Framework-for-Robust-Dalrymple-Skalse/d81e8d1d3c8acbcf9755ef470098b9c02adf5963) [arxiv](https://arxiv.org/html/2405.06624v2)

- a world model describing how the AI affects the world; [arxiv](https://arxiv.org/html/2405.06624v2)
- a safety specification expressed in terms of the world model; [arxiv](https://arxiv.org/html/2405.06624v2)
- a verifier producing an "auditable proof certificate" or quantitative bound relative to the world model. [alphaxiv](https://www.alphaxiv.org/abs/2405.06624) [arxiv](https://arxiv.org/html/2405.06624v2)

A later version adds deployment infrastructure as a fourth component. The paper grades world models and specifications on levels of rigour, from none to formally verified. [berkeley](https://www2.eecs.berkeley.edu/Pubs/TechRpts//2024/EECS-2024-45.pdf)

**Related proposals.**

- Tegmark and Omohundro ("Provably Safe Systems", 2023) argue for proof-carrying behaviour.
- Bengio et al. ("Can a Bayesian Oracle Prevent Harm from an Agent?", arXiv:2408.05284) bound harm probability using a posterior over theories, taking cautious maxima over plausible theories rather than the expected value. [arxiv](https://arxiv.org/pdf/2408.05284) This is the precursor of the Scientist AI proposal (Bengio et al. 2025), a non-agentic explanatory model used as a guardrail on agents.
- Russell (Human Compatible 2019) gives assistance games.

**Comparison with jack.** jack has a verifier (the kernel) of the record, a specification (the charter) mostly in prose, and a world model (the world types) entirely in prose. In GS AI's terms, the guarantee covers syntax and provenance, not world effects. The GS AI ladder gives jack the vocabulary to state this precisely and to set targets.

The imports are:

- the explicit three-way separation, with world types promoted from prose to typed LoA schemas (§4);
- Bengio's cautious-bound idea for resolution: when resolvers disagree, resolve to the pessimistic (annul or 0) outcome rather than average;
- the "gatekeeper" pattern from the ARIA Safeguarded AI programme, in which nothing acts in the world without a verifier certificate. jack already has this for the trusted base.

**Verdict.** Do not chase formal world models for web outcomes. GS AI concedes that the world model is the hardest component. Treat it as a ceiling, not a requirement.

### 16. Reward hacking and defences for a saturable promotion statistic (G6)

**Formal results.**

- Skalse, Howe, Krasheninnikov and Krueger ("Defining and Characterizing Reward Hacking", NeurIPS 2022) define a proxy as unhackable if increasing proxy return can never decrease true return. They prove that over all stochastic policies, two reward functions are unhackable only if one is constant. Non-trivial unhackable pairs exist only on restricted (finite or deterministic) policy sets. [arxiv](https://arxiv.org/abs/2209.13085)
- Pan, Bhatia and Steinhardt ("The Effects of Reward Misspecification", ICLR 2022) find phase transitions: more capable optimisers hack more, sometimes abruptly.
- Gao, Schulman and Hilton ("Scaling Laws for Reward Model Overoptimization", ICML 2023) fit functional forms for gold reward as a function of KL distance from the initial policy. Gold reward rises then falls.
- Karwowski et al. ("Goodhart's Law in Reinforcement Learning", ICLR 2024) give an early-stopping method with provable regret bounds.
- Hennessy and Goodhart ("Goodhart's Law and Machine Learning: A Structural Perspective", International Economic Review 2023) give the structural-econometrics version.
- Zhuang and Hadfield-Menell ("Consequences of Misaligned AI", NeurIPS 2020) prove that when a proxy references only a subset of the attributes of utility and resources are constrained, optimisation drives unreferenced attributes to their minimum and utility can become arbitrarily low.

**Mitigations.** Taylor's quantilisers ("Quantilizers", AAAI Workshop 2016) sample from the top q-fraction of a trusted base distribution rather than maximise. Expected cost under any cost function is bounded by 1/q times the base distribution's expected cost.

**Pre-stated attack list for jack's statistics.** The literature supports the following list, each item with its formal source:

| Attack | Source | Mechanism in jack | Defence |
|---|---|---|---|
| Schedule saturation | Gao et al. 2023; Zhuang & Hadfield-Menell 2020 | forecasts on near-certain, high-frequency events inflate E | claims sampled by a party other than the forecaster; per-claim difficulty adjustment (as ForecastBench does) |
| Constant entrant | Kong–Schoenebeck uninformative equilibria | a proposer emitting fixed probabilities on a stream where the null is miscalibrated | null fitted and committed on held-out history; constant-forecaster baseline must itself be beaten |
| Collusion among proposers or resolvers | Kong & Schoenebeck 2018; Gao et al. 2014; AI-control untrusted monitoring | same-family sessions agree on readings | cross-family resolvers; multi-task agreement scoring minus agreement on unrelated tasks |
| Steering the decision | Othman & Sandholm 2010; Chen et al. 2014 | forecasts influence which layer is promoted | randomised promotion with full support; importance-weighted scores |
| Choice of null or stream after data | Gelman & Loken | e-process valid only for a committed null | single pre-registration entry per window |
| Percept tampering | Everitt et al. 2016 | resolver saves a page the URL never served | TLS provenance (DECO-style), third-party archive witness |
| Performative outcomes | Perdomo et al. 2020 | sovereign-operated stream | exclusion or committed dither (§10) |
| Optimiser over-pressure | Pan et al. 2022; Karwowski et al. 2024 | many proposer variants searched against one stream | cap on proposals per window; quantilised selection among proposers |

Quantilisation is the right default for the proposer election. Hedge already mixes, but its weights concentrate. A floor on mixing (Fixed Share, already used) is a crude quantiliser and should be justified in those terms.

### 17. Rule-based governance of LLM agents and the agent-infrastructure stack

**Model-level rule governance.**

- Constitutional AI (Bai et al. 2022) trains on model self-critique against written principles.
- Collective Constitutional AI (Huang et al., FAccT 2024) sources the principles from the public.
- OpenAI's Model Spec (2024 onward) is a published behavioural specification.
- Deliberative alignment (Guan et al. 2024) trains models to reason over the specification.
- Rule-based rewards (Mu et al. 2024) turn rules into reward signals.

All of these govern model dispositions. None governs an agent's institutional record, so they are complementary to jack and not substitutes.

**Audit literature.**

- Raji et al. ("Closing the AI Accountability Gap", FAT* 2020) give the SMACTR internal-audit framework.
- Mökander and Floridi ("Ethics-Based Auditing of Automated Decision-Making Systems", Minds and Machines 2021) cover ethics-based auditing.
- Shevlane et al. ("Model Evaluation for Extreme Risks", 2023) cover dangerous-capability evaluation.

**Pre-stated thresholds.** Anthropic's Responsible Scaling Policy (v1 September 2023; per Anthropic's RSP version list, v2.0 effective 15 October 2024, v2.1 31 March 2025 and v2.2 14 May 2025) maps Capability Thresholds (for example CBRN-3/4, AI R&D-4/5) to Required Safeguards (ASL-N standards). Version 2.1 commits that if a model cannot be shown "sufficiently below the relevant Capability Thresholds", Anthropic will "upgrade to the ASL-3 Required Safeguards… and conduct a follow-up capability assessment". [anthropic](https://www-cdn.anthropic.com/17310f6d70ae5627f55313ed067afc1a762a4068.pdf) ASL-3 protections were activated in May 2025. [elephas](https://elephas.app/resources/anthropic-rsp-v3-policy-change) Version 3.0, which Anthropic's own RSP page lists as "effective February 24, 2026" and describes as "a comprehensive rewrite of the RSP", restructures commitments and redefines "ASL" as safeguard groupings; the current version is v3.4, effective 8 July 2026, following v3.1 (2 April), v3.2 (29 April) and v3.3 (26 May).

Google DeepMind's Frontier Safety Framework (v1 May 2024 to v3.1 April 2026) defines Critical Capability Levels per domain (CBRN, cyber, harmful manipulation, ML R&D, misalignment). [metr](https://metr.org/common-elements) [arxiv](https://arxiv.org/pdf/2507.06261) [deepmind](https://deepmind.google/blog/strengthening-our-frontier-safety-framework/) It adds alert thresholds "significantly below" each CCL and, in v3.1, Tracked Capability Levels below them. [Substack](https://frontierrisk.substack.com/p/google-deepminds-frontier-safety) [arxiv](https://arxiv.org/pdf/2507.06261) [vorplabs](https://vorplabs.com/ai-regulatory-updates/deepmind-frontier-safety-framework)

These are the institutional precedent for jack's pre-stated windows. Their weakness is the same as jack's: thresholds are amended by the party they bind.

**Agent-infrastructure standards (2025–2026)** now supply pieces jack builds by hand:

- **Agent Payments Protocol (AP2), Google, 16 September 2025.** It introduces "verifiable credentials called 'mandates' that act as secure digital contracts between you, the agent, and the merchant". These are signed Intent and Cart mandates, which are non-repudiable records of what a principal authorised. Google's own blog post of 28 April 2026 confirms "we're donating the Agent Payments Protocol (AP2) to the FIDO Alliance". The same day Google released AP2 v0.2, which adds "Human Not Present" payments, and also donated Verifiable Intent, co-developed with Mastercard. AP2 gives signed evidence, not an append-only log.
- **Visa Trusted Agent Protocol, 14 October 2025, with Cloudflare.** It uses "agent-specific cryptographic signatures" built on HTTP Message Signatures (RFC 9421) and Web Bot Auth, and signs agent identity and intent into requests.
- **Agentic Commerce Protocol, OpenAI and Stripe, 29 September 2025.** It provides delegated payment tokens scoped to one merchant and capped at the checkout total. This is a capability, not an audit record.
- **Agent2Agent (A2A), Linux Foundation project since 23 June 2025.** It covers inter-agent messaging and Agent Cards. AGNTCY, also at the Linux Foundation, targets "discovery, identity, messaging, and observability" for agents.
- **IETF drafts.** draft-oauth-ai-agents-on-behalf-of-user "enhances auditability through access token claims that document the delegation chain from the user to the agent". WIMSE-based agent identity drafts and delegation-chain drafts enforce "monotonic attenuation, bounded depth, monotonic expiry, and principal invariance". All are individual or working-group drafts, not standards.
- **IETF SCITT (Supply Chain Integrity, Transparency and Trust).** It defines signed statements, transparency services and receipts. The IETF SCITT datatracker lists individual drafts that profile it for agent actions, including draft-emirdag-scitt-ai-agent-execution ("AI Agent Execution Profile of SCITT", Emirdag, April 2026: "tamper-evident records of autonomous AI agent actions… hash chain integrity, temporal ordering, and sequence completeness"), draft-mih-scitt-agent-action-capsule-05 (26 September 2026), draft-noa-scitt-ai-agent-receipt-01 (14 August 2026) and draft-munoz-scitt-permit-profile-01 (pre-execution authorisation records, 19 July 2026). A companion audit-architecture draft states that "the Transparency Log binds a record to an append-only, non-equivocating statement sequence". The only SCITT working-group drafts with the IESG are draft-ietf-scitt-scrapi and draft-ietf-scitt-receipts-ccf-profile, and neither is agent-specific.
- **"Know Your Agent".** It originates academically with Chaffer (2025), and there are vendor frameworks such as Vouched's KYA-OS, which "issues delegations as Ed25519-signed W3C VC-JWTs" and was donated to the Decentralized Identity Foundation. No regulator has adopted a KYA rule.

**Verdict.** jack's log is a single-writer transparency log without witnesses. The one property it lacks relative to Certificate Transparency (RFC 6962/9162) and SCITT is non-equivocation against its own owner. A sovereign could present different signed histories to different auditors. Adopt witness cosigning of periodic checkpoints (signed tree heads) by at least one party outside the owner's control, and emit SCITT-compatible receipts. Do not reinvent the receipt format. Adopt AP2-style signed mandates only if jack's agents transact; otherwise they are irrelevant.

### 18. Cybernetic and biological loops: what is more than metaphor

**Theory.**

- Autopoiesis (Maturana & Varela 1980) and its legal offshoots (§11) are descriptive frameworks.
- Pattee's "semantic closure" (1982; 1995) holds that a self-replicating system needs both rate-independent symbolic constraints and rate-dependent dynamics, coupled by a code. This is a framework with one transferable point. jack's kernel is the rate-independent symbolic layer and the world is the dynamics. Pattee's point that the coupling (measurement) cannot be reduced to either is the epistemological statement of G3.
- Hofstadter (Gödel, Escher, Bach 1979; I Am a Strange Loop 2007) is metaphor only.
- Friston's free-energy principle ("The free-energy principle: a unified brain theory?", Nature Reviews Neuroscience 2010) and Markov-blanket formalism (Kirchhoff et al., J. R. Soc. Interface 2018) describe self-maintaining boundaries. Bruineberg, Dołęga, Dewhurst and Baltieri ("The Emperor's New Markov Blankets", BBS 2022) argue that the formalism conflates a statistical tool with a metaphysical boundary.

**Built systems.** Active-inference agents exist (for example the pymdp library, Heins et al., JOSS 2022), and some include hierarchical self-models. None offers a mechanism for an institution's self-measurement that the e-process and scoring machinery does not already provide better.

**Verdict.** Ignore this cluster for design. Cite Pattee once for the irreducibility of measurement and Luhmann once for operational-closure drift.

## Master map

| Concept / result | Canonical source(s) | Establishes (status) | jack construct | Status in jack | Import / don't reinvent | Misapplied if |
|---|---|---|---|---|---|---|
| Undefinability of truth | Tarski 1933 | no self-truth predicate in rich language (theorem) | kernel / SPEC | applied (stratified by time) | none needed | applied to finite decidable kernel as if threatened |
| Grounded partial truth | Kripke 1975 | least fixed point; grounded sentences valued (theorem) | forecasts about the court | partial | rule: no forecast on statistic its own entry feeds | used to justify self-scoring |
| Revision theory | Gupta & Belnap 1993 | stable vs oscillating truth (framework) | iterated world-type readings | missing | detect oscillating readings across resolvers | treated as resolution method |
| Rule-following / open texture | Wittgenstein 1953; Kripke 1982; Waismann 1945; Hart 1961 | no rule fixes its application (framework) | world types | missing (G1) | annul penumbra cases | used to excuse retroactive reading |
| Interpretivism vs rules | Dworkin 1986; Schauer 1991 | retroactive best-reading vs entrenched text (framework) | resolver reading | implicit Dworkinian | adopt Schauer: text binds | Dworkin used for resolution |
| Reason model of precedent | Horty 2011 | constraint by accumulated reason ordering (formal model) | resolutions as precedents | missing | precedent ledger binding later forecasts only | precedents applied retroactively |
| Normative systems | Alchourrón & Bulygin 1971 | gaps and inconsistencies formalised (formal theory) | `spec_conflict` | partial | add gap report | gaps silently filled |
| Input/output logic | Makinson & van der Torre 2000 | conditional norms separate from fact logic (formal logic) | windows | missing (G7) | formalise window rules | used for kernel (unnecessary) |
| Tû-Tû | Ross 1957 | legal terms as inference tickets (framework) | "repair", "object", "stated end" | missing (G7) | define by condition→consequence fields | treated as essences |
| Jural relations | Hohfeld 1913 | 8 relations (framework) | key powers, trusted base | implicit | type enforcement map by Hohfeld | — |
| Versioned contract meaning | parol evidence; contra proferentem | meaning fixed at formation (legal practice) | `forecast` | missing (G1) | `world_types_hash`; construe against drafter | drafter = forecaster ignored |
| Resolution-criteria practice | Metaculus FAQ; Polymarket/UMA disputes | annul vs stretch; voter conflicts (practice) | `resolution` | missing | add annulled outcome | annulment used to dodge losses |
| Deontic scorekeeping | Brandom 1994; Kibble 2006 | commitments/entitlements (framework) | log as ledger | applied in effect | cite; no build | accommodation allowed |
| Accommodation | Lewis 1979 | score shifts to fit utterance (framework) | resolver reading | unguarded | forbid accommodation | — |
| Commitment ACLs | Singh 1999/2000; Fornara & Colombetti 2002 | social semantics of commitments (formal) | forecast/resolution types | parallel | reuse commitment lifecycle states | mentalistic reading of LLM |
| Electronic institutions | Esteva et al. 2001/2008; Noriega & de Jonge 2016 | spec-to-runtime institution engineering (tooling) | charter + judge | parallel | borrow metamodel, not software | adopting legacy middleware |
| Institutional grammar | Crawford & Ostrom 1995; Frantz et al. 2013 | ADICO/nADICO rule schema (framework) | maxims, enforcement map | missing (G7) | encode every clause as ADICO record | used as mere counting |
| Statute DSLs | Catala (Merigoux et al. 2021); LegalRuleML | executable law text (tooling) | windows SPEC | missing (G7) | write windows in Catala/Datalog | formalising the charter's spirit |
| Levels of abstraction | Floridi 2008 | claims relative to typed observables (method) | world types | missing | typed LoA per world type | — |
| Claim decomposition | FActScore 2023; SAFE 2024 | atomic claim verification gains (empirical) | claim string | missing | split compound claims at entry | decomposition after outcome |
| Operational subjectivism | de Finetti 1937/1974 | probability = enforced betting quotient (framework) | forecasts (G2) | partly | score procedures, drop "merit" | template treated as believer |
| LLM calibration | Kadavath 2022; Tian 2023; Xiong 2024 | post-training miscalibration (empirical) | proposers | unmeasured | record model+date; calibrate per procedure | treated as stationary |
| LLM forecasting | Halawi 2024; Karger 2025 | near-parity with experts, contested (empirical) | proposers | — | benchmark proposers against ForecastBench-style baselines | parity claims over-read |
| Peer prediction / BTS | Miller–Resnick–Zeckhauser 2005; Prelec 2004 | truthful equilibrium w/o outcomes (theorem) | resolvers (G3) | missing | multi-task agreement scoring | used for forecasts with outcomes |
| Uninformative equilibria | Kong & Schoenebeck 2018; Gao et al. 2014 | collusion equilibria exist (theorem/empirical) | two-resolver agreement | unguarded | focal-truth mechanisms; cross-family | agreement treated as evidence |
| Self-resolving markets | Srinivasan, Karger & Chen 2025 | IC without outcome (theorem, strong assumptions) | "repairs → 0" | missing | only for unresolvable claims | later reporters not better informed |
| Problem of the criterion | Sextus; Chisholm 1973 | no neutral meta-criterion (framework) | windows' criteria | implicit | record paradigm cases (particularism) | presented as solved |
| Epistemic circularity | Alston 1986/1993; Bergmann 2004; Vogel 2000 | benign vs bootstrapping (framework) | wealth process | partial | outcome-independence test per stream | cron stream counted |
| Coherence impossibility | Olsson 2005; Bovens & Hartmann 2003 | coherence not truth-conducive w/o independent credibility (theorem) | two-checker agreement | partial | independence audit | agreement of same-family checkers |
| Independence for juries | Dietrich & Spiekermann 2013; Ladha 1992 | independence conditional on common causes (theorem) | resolvers, checkers | applied to kernel only (G3) | diversity on measurement | counting sessions not causes |
| Reliabilism | Goldman 1979 | justify processes not beliefs (framework) | resolver procedure | missing | measured resolver error on audits | — |
| Epistemic iteration | Chang 2004; Tal 2013/2017 | coherentist progress of standards (framework) | window amendments | implicit | principle of respect per amendment | used to excuse churn |
| Construct/consequential validity | Cronbach & Meehl 1955; Messick 1989 | validity incl. consequences (framework) | E as value measure | missing (G5) | validity argument for E | liveness taken for value |
| Surrogate endpoints | Prentice 1989; Fleming & DeMets 1996; Buyse & Molenberghs 1998 | surrogate must capture full effect (criterion/empirical) | E → promotion → repairs | missing (G5) | scored preservation claim; cross-layer association | single-layer validation |
| Research programmes | Lakatos 1970; Popper 1959 | progressive vs degenerating (framework) | clause minting | missing | amendment carries forecast; lapse on failure | used rhetorically |
| Pre-registration | Nosek et al. 2018; Chambers 2013; Scheel et al. 2021 | commitment changes results (empirical) | windows | partial | single pre-registration entry | e-process thought sufficient |
| Reflection / Dutch book | van Fraassen 1984 | diachronic coherence (theorem) | forecasts about court | missing | notice periods for amendments | applied to non-agents |
| Performative prediction | Perdomo et al. 2020 | stability ≠ optimality; convergence conditions (theorem) | `world.renavon` | missing (G4) | exclude or stabilise | ignored for owner streams |
| Closed-loop identification | Forssell & Ljung 1999 | external excitation required (theorem) | owner-operated stream | missing (G4) | committed randomised dither | identification claimed from feedback data |
| Lucas critique | Lucas 1976 | regime change breaks estimates (framework) | amendments mid-window | partial | new window per amendment | — |
| Grundnorm / rule of recognition | Kelsen 1934; Hart 1961 | regress ends in presupposition/social fact (framework) | genesis, sovereign key | applied | none | — |
| Normal justification thesis | Raz 1986 | authority legit iff improves conformity to reasons (framework) | court legitimacy | missing (G5) | measure court vs owner-unaided | — |
| Autopoietic law | Luhmann 2004; Teubner 1993 | operational closure (descriptive) | ratio guard | applied | none | used as design spec |
| Law as coordination | Hadfield & Weingast 2012 | stable, public rules (model) | charter | partial | amendment rate limits | — |
| Time inconsistency | Kydland & Prescott 1977 | discretion worse than rules (theorem) | `amend` | missing | lagged effect, no open windows | — |
| Self-amendment | Ross 1969; Suber 1990 | acceptance vs inference model (analysis) | `transmute`→`amend` | applied | entrenchment rule for amendment clause | Ross's paradox treated as fatal |
| Incomplete contracts | Grossman–Hart 1986; Hadfield-Menell & Hadfield 2019 | residual rights; external gap-filling (theory) | sovereign, world types | applied | non-retroactive gap filling | gap-filling retroactive |
| Multitask incentives | Holmström & Milgrom 1991 | high-powered measured incentives crowd out (theorem) | E ≥ 20 promotion | missing (G5) | goal-sampled streams; lower power | — |
| Decision markets | Othman & Sandholm 2010; Chen et al. 2014 | deterministic rules manipulable; randomise (theorem) | promotion | missing (G6) | full-support randomised promotion | — |
| Embedded agency / tiling | Demski & Garrabrant 2019; Yudkowsky & Herreshoff 2013 | Löbian obstacle (theorem/framework) | self-modification | sidestepped | none (evidence not proof) | proof-based approval attempted |
| Self-modification safety | Everitt et al. 2016; Tětek et al. 2020 | safe iff current utility evaluates (theorem); fails bounded | trunk judge | applied | guard percepts | percept tampering ignored |
| AI control | Greenblatt et al. 2024; Bhatt et al. 2025 | protocol safety vs red team (empirical method) | parties, judge | partial | control evaluations, audit budget | LLM monitor trusted as code |
| Debate | Irving et al. 2018; Khan et al. 2024 | debate aids weaker judges (empirical) | disputed resolutions | missing | cross-family debate before sovereign | — |
| Guaranteed Safe AI | Dalrymple et al. 2024 | world model/spec/verifier separation (framework) | world types/charter/kernel | partial | state rigour level per component | demanding formal web world model |
| Bayesian oracle | Bengio et al. 2024 | cautious harm bounds (proposal/theorem) | resolution disagreement | missing | pessimistic resolution | — |
| Reward hacking | Skalse et al. 2022; Zhuang & Hadfield-Menell 2020 | unhackability nearly impossible (theorem) | E | missing (G6) | attack list | belief that a clever proxy is safe |
| Overoptimisation | Gao et al. 2023; Pan et al. 2022; Karwowski 2024 | proxy-gold divergence laws (empirical/theorem) | proposer search | missing | cap search; early stop | — |
| Quantilisers | Taylor 2016 | bounded cost vs base (theorem) | Hedge election | partial (Fixed Share) | justify floor as quantile | — |
| Transparency logs | RFC 6962/9162; IETF SCITT | non-equivocation via witnesses (standard) | `log.jsonl` | partial | witness cosigning, SCITT receipts | single-writer log treated as CT |
| Signed mandates | AP2 2025 | non-repudiable authorisation (spec) | `key`, powers | parallel | only if transacting | — |
| Frontier thresholds | Anthropic RSP; GDM FSF | pre-stated capability thresholds (practice) | windows | parallel | alert thresholds below promotion | amended by bound party |
| Semantic closure | Pattee 1982/1995 | symbol/dynamics coupling irreducible (framework) | measurement | — | cite only | — |
| Free energy / blankets | Friston 2010; Bruineberg et al. 2022 | contested formalism | none | — | ignore | used as design |
| Strange loops | Hofstadter 1979 | metaphor | none | — | ignore | — |

## Prioritised imports

1. **Versioned world types (G1).** Add `world_types_hash` and `resolver_model` fields to `forecast` and `resolution`. Amendments bind only later forecasts. Mechanism: parol evidence rule plus the kernel's existing non-retroactivity predicate, extended to one more field.
2. **Annulment outcome and contra proferentem (G1).** Add a third resolution value, `annulled`, excluded from log-loss and wealth, used when the outcome falls outside the hashed text, as in Metaculus practice. Construe ambiguity against the drafter.
3. **Precedent ledger (G1).** Penumbra resolutions enter a reason ordering that binds later forecasts only. Mechanism: Horty's 2011 reason model.
4. **Scored preservation claim (G5).** For each layer, enter a forecast linking promotion to owner-repair reduction over a stated horizon, and accumulate cross-layer association between E and repairs. Mechanism: Prentice criterion validated Buyse–Molenberghs-style, with Raz's normal-justification comparison against the owner's unaided judgement.
5. **Goal-sampled promotion streams (G5).** Promotion requires E on streams whose claims are sampled from the owner-goal set by a party other than the proposer. Liveness streams are reported separately and never promote. Mechanism: Holmström–Milgrom; Zhuang–Hadfield-Menell.
6. **Pre-registered attack list and control evaluation (G6).** Commit the §16 table on the log and run red-team control evaluations against each window before it opens. Mechanism: Greenblatt et al. 2024 protocol evaluation.
7. **Randomised promotion with full support (G6).** Promote by a rule that gives every eligible layer positive probability, with scores importance-weighted. Mechanism: Chen, Kash, Ruberry and Shnayder 2014.
8. **Single pre-registration entry per window (G6, G5).** Null, stream, claim-sampling rule and threshold are committed together. Any amendment opens a new window with separate wealth. Mechanism: registered reports, paired with e-processes.
9. **Measurement diversity (G3).** Use two resolvers of different families via different fetch paths, plus TLS-provenance or third-party-archive witnesses. Score agreement multi-task style so that blind agreement is not rewarded. Mechanisms: Dietrich–Spiekermann; DECO; Kong–Schoenebeck.
10. **Closed-loop rule for owner streams (G4).** Exclude sovereign-operated streams from promotion evidence, or commit a randomised dither schedule and count only dither-dependent outcomes. Mechanism: Forssell–Ljung; Perdomo et al.
11. **ADICO-typed charter and enforcement map (G7).** Each clause is an (A, D, I, C, O) record. "O" points to a code pin or is marked `hand`, and powers are typed by Hohfeld. Mechanism: Crawford–Ostrom, nADICO.
12. **Formal window specification (G7).** Write windows in Catala or Datalog, with "repair" and "object" defined as Tû-Tû condition→consequence rules and each world type given a typed Floridi LoA. Differentially test the windows against a second implementation, as for the kernel.
13. **Witnessed checkpoints (record integrity against the owner).** Have an external witness cosign periodic signed tree heads, and emit SCITT-compatible receipts. Mechanism: RFC 6962/9162; IETF SCITT.
14. **Amendment discipline.** Every `amend` carries a forecast of its effect and lapses if the forecast fails. Amendments take effect after a notice lag and never on open windows. Mechanism: Lakatos; Kydland–Prescott; sunset clauses.
15. **Cautious resolution under disagreement.** When resolvers disagree, annul or take the pessimistic outcome rather than averaging. Mechanism: Bengio et al.'s Bayesian-oracle cautious bound.

## Annotated reading list

**Primary and canonical sources**

1. Tarski, A. (1933/1956) "The Concept of Truth in Formalized Languages" — why the kernel's metalanguage must sit above its object language.
2. Kripke, S. (1975) "Outline of a Theory of Truth", J. Phil. — groundedness as the criterion for permissible self-reference.
3. Gupta, A. & Belnap, N. (1993) *The Revision Theory of Truth* — oscillating readings as a diagnostic.
4. Field, H. (2008) *Saving Truth from Paradox* — the cost of keeping naïve truth; mostly for completeness.
5. Wittgenstein, L. (1953) *Philosophical Investigations* §§185–242 — no rule fixes its own application.
6. Kripke, S. (1982) *Wittgenstein on Rules and Private Language* — community correctness and its limits.
7. Waismann, F. (1945) "Verifiability" — origin of "open texture".
8. Hart, H.L.A. (1958) "Positivism and the Separation of Law and Morals"; (1961) ch. VII — core and penumbra.
9. Dworkin, R. (1986) *Law's Empire* — interpretivism, the model to avoid for resolution.
10. Schauer, F. (1991) *Playing by the Rules* — why entrenched text beats best reading for predictability.
11. Horty, J. (2011) "Rules and Reasons in the Theory of Precedent", Legal Theory — implementable precedent constraint.
12. Alchourrón, C. & Bulygin, E. (1971) *Normative Systems* — gaps and inconsistencies formalised.
13. Makinson, D. & van der Torre, L. (2000) "Input/Output Logics", J. Phil. Logic — logic for conditional norms.
14. Ross, A. (1957) "Tû-Tû", Harvard Law Review — defining terms by inference tickets.
15. Hohfeld, W.N. (1913) "Some Fundamental Legal Conceptions", Yale LJ — typing powers and immunities.
16. Ross, A. (1969) "On Self-Reference and a Puzzle in Constitutional Law", Mind — the self-amendment paradox.
17. Suber, P. (1990) *The Paradox of Self-Amendment* — acceptance vs inference models; Nomic.
18. Brandom, R. (1994) *Making It Explicit* — deontic scorekeeping.
19. Lewis, D. (1979) "Scorekeeping in a Language Game" — accommodation, the G1 mechanism.
20. Searle, J. (1995) *The Construction of Social Reality* — constitutive rules.
21. Crawford, S. & Ostrom, E. (1995) "A Grammar of Institutions", APSR — ADICO.
22. Harnad, S. (1990) "The Symbol Grounding Problem", Physica D — what jack need not solve.
23. Floridi, L. (2008) "The Method of Levels of Abstraction", Minds and Machines — typed observables for world types.
24. de Finetti, B. (1974) *Theory of Probability* — probability without a believer.
25. Murphy, A.H. (1973) "A New Vector Partition of the Probability Score" — calibration vs resolution.
26. Prelec, D. (2004) "A Bayesian Truth Serum for Subjective Data", Science — elicitation without outcomes.
27. Miller, N., Resnick, P. & Zeckhauser, R. (2005) "Eliciting Informative Feedback: The Peer-Prediction Method" — the base mechanism.
28. Chisholm, R. (1973) *The Problem of the Criterion* — particularism.
29. Alston, W. (1993) *The Reliability of Sense Perception* — benign epistemic circularity.
30. Vogel, J. (2000) "Reliabilism Leveled", J. Phil. — the bootstrapping objection.
31. Goldman, A. (1979) "What is Justified Belief?" — reliabilism for resolver processes.
32. Olsson, E. (2005) *Against Coherence* — coherence needs independent credibility.
33. Dietrich, F. & Spiekermann, K. (2013) "Independent Opinions?", Mind — what independence means.
34. Chang, H. (2004) *Inventing Temperature* — epistemic iteration and the principle of respect.
35. Tal, E. (2013) "Old and New Problems in Philosophy of Measurement", Philosophy Compass — coherentist, model-based calibration.
36. Cronbach, L. & Meehl, P. (1955) "Construct Validity in Psychological Tests" — construct validity.
37. Messick, S. (1995) "Validity of Psychological Assessment", American Psychologist — consequential validity.
38. Prentice, R. (1989) "Surrogate Endpoints in Clinical Trials", Stat. Med. — surrogate criterion.
39. Fleming, T. & DeMets, D. (1996) "Surrogate End Points in Clinical Trials: Are We Being Misled?" — how surrogates fail.
40. Lakatos, I. (1970) "Falsification and the Methodology of Scientific Research Programmes" — progressive vs degenerating amendment.
41. Gelman, A. & Loken, E. (2014) "The Statistical Crisis in Science", American Scientist — forking paths.
42. Nosek, B. et al. (2018) "The Preregistration Revolution", PNAS — commitment before data.
43. van Fraassen, B. (1984) "Belief and the Will", J. Phil. — Reflection.
44. Lucas, R. (1976) "Econometric Policy Evaluation: A Critique" — regime dependence.
45. Forssell, U. & Ljung, L. (1999) "Closed-Loop Identification Revisited", Automatica — identification under feedback.
46. Kydland, F. & Prescott, E. (1977) "Rules Rather than Discretion", JPE — time inconsistency.
47. Raz, J. (1986) *The Morality of Freedom* — normal justification thesis.
48. Hadfield, G. & Weingast, B. (2012) "What is Law?", J. Legal Analysis — law as coordination.
49. Holmström, B. & Milgrom, P. (1991) "Multitask Principal–Agent Analyses", JLEO — crowding-out theorem.
50. Grossman, S. & Hart, O. (1986) "The Costs and Benefits of Ownership", JPE — residual control rights.

**AI and agent papers (2016–2026)**

51. Everitt, T., Filan, D., Daswani, M. & Hutter, M. (2016) "Self-Modification of Policy and Utility Function in Rational Agents" — the condition jack implements.
52. Demski, A. & Garrabrant, S. (2019) "Embedded Agency" — problem map.
53. Fallenstein, B. & Soares, N. (2015) "Vingean Reflection" — why proof-based self-trust stalls.
54. Hadfield-Menell, D. & Hadfield, G. (2019) "Incomplete Contracting and AI Alignment", AIES — contracts frame.
55. Perdomo, J., Zrnic, T., Mendler-Dünner, C. & Hardt, M. (2020) "Performative Prediction", ICML — G4 formalism.
56. Zhuang, S. & Hadfield-Menell, D. (2020) "Consequences of Misaligned AI", NeurIPS — incomplete proxies.
57. Skalse, J. et al. (2022) "Defining and Characterizing Reward Hacking", NeurIPS — unhackability theorem.
58. Gao, L., Schulman, J. & Hilton, J. (2023) "Scaling Laws for Reward Model Overoptimization", ICML — divergence laws.
59. Greenblatt, R., Shlegeris, B., Sachan, K. & Roger, F. (2024) "AI Control", ICML — protocol evaluation method.
60. Dalrymple, D. et al. (2024) "Towards Guaranteed Safe AI" — component separation.
61. Kong, Y. & Schoenebeck, G. (2018) "Equilibrium Selection in Information Elicitation without Verification", ITCS — collusion-resistant elicitation.
62. Srinivasan, S., Karger, E. & Chen, Y. (2025) "Self-Resolving Prediction Markets for Unverifiable Outcomes", EC — scoring without outcomes.
63. Chen, Y., Kash, I., Ruberry, M. & Shnayder, V. (2014) "Eliciting Predictions and Recommendations for Decision Making", ACM TEAC — randomised decision rules.
64. Karger, E. et al. (2025) "ForecastBench", ICLR — LLM forecasting baseline.
65. Purushothama, A. et al. (2025) "Prompting from the Bench" — LLM interpretation instability.
66. Kibble, R. (2006) "Speech Acts, Commitment and Multi-Agent Communication" — Brandom applied to agents.
67. Esteva, M. et al. (2008) "Electronic Institutions Development Environment" — institution tooling precedent.
68. Merigoux, D., Chataing, N. & Protzenko, J. (2021) "Catala: A Programming Language for the Law", ICFP — executable rule text.
69. Taylor, J. (2016) "Quantilizers" — mild optimisation.
70. IETF SCITT architecture and draft-emirdag-scitt-ai-agent-execution (2026) — standard receipts for agent action logs.

## Open questions the literature does not settle

**Meta-criterion for windows.** No principled meta-criterion for choosing a court's evaluation criteria exists. Chisholm's particularism and Chang's principle of respect are disciplines, not solutions. Whether the owner's paradigm cases should themselves be amendable is unaddressed.

**Valid e-processes over a stream of amendments.** There is no theorem combining e-process validity with a null that is itself amended by a party who has seen the data. Fresh windows per amendment are conservative but waste evidence. A formal treatment of "amended nulls" with valid accumulation seems not to exist.

**Independence among LLM resolvers.** Whether model families from different labs are independent in the Dietrich–Spiekermann sense is an open empirical question. Shared pretraining corpora suggest substantial common cause, and no published measurement of cross-family error correlation on resolution tasks was found.

**Interpretation drift across model versions.** The legal-LLM literature shows instability across prompts and post-training. It does not show whether the drift in readings of a fixed text across versions of the same model is bounded. jack's versioning makes this measurable, but no prior measurement exists.

**Preservation claims on long horizons.** Surrogate validation needs many interventions with observed true endpoints. A single owner with a handful of layers may never accumulate enough for Buyse–Molenberghs-style evidence. Self-resolving markets offer an alternative only under assumptions jack's proposers do not obviously meet.

**Self-amendment rates.** No empirical literature identifies an optimal rate of self-amendment for small institutions. Sunset evidence is mixed, and amendment budgets are unstudied.

## Caveats

**Weak sourcing.** Several 2025–2026 items rest on secondary reporting:

- the UMA vote concentration and the WSJ voter-linkage figures;
- the detail of Anthropic RSP v3.0's restructuring (its dates and status as "a comprehensive rewrite" are confirmed by Anthropic's own RSP page);
- the Forecasting Research Institute's parity claim, which its authors describe as not statistically significant.

The AP2–FIDO donation is confirmed by Google's own 28 April 2026 announcement. Treat the rest as indicative. IETF agent drafts are individual submissions and may lapse.

**Status judgements.** Status judgements for jack are inferred from the project description supplied, not from the repository.

**Proposals, not results.** Recommendations marked as proposals rather than established results are the amendment budget, cautious resolution and Tû-Tû field definitions. They are defensible by analogy but untested.