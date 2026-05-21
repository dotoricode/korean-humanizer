# korean-humanizer

This context defines the project language around the Korean writing humanizer and how related external demos should be described.

## Language

**korean-humanizer**:
A Korean-specific prompt and skill that edits AI-written Korean to sound more natural while preserving meaning.
_Avoid_: generic humanizer, official hosted service

**Third-party community demo**:
An external service operated outside this repository that lets users try korean-humanizer before installation.
_Avoid_: official demo, official service, hosted korean-humanizer

**Official demo**:
A demo operated or endorsed by this repository as the project's own service.
_Avoid_: community demo, third-party service

**Sentence merging**:
Combining two adjacent sentences into one when they express the same idea, resulting in a shorter, more direct sentence. Allowed only when both conditions hold: (1) the two sentences are semantically redundant, and (2) the merge makes the sentence shorter. Not the same as rewriting — the merged sentence must stay close to the original wording.
_Avoid_: restructuring, rewriting, paraphrasing

**Pronoun preservation**:
Keeping subject pronouns (e.g. "저희", "우리") in formal writing contexts (email, B2B) even when they seem redundant. Removing them makes the tone feel cold or impersonal.
_Avoid_: pronoun deletion, subject dropping

**Honorific modifier preservation**:
Keeping honorific verb modifiers (e.g. "보내주신", "말씀하신") attached to nouns in formal or semi-formal contexts. Stripping them removes courtesy signals that are intentional, not AI-ish.
_Avoid_: honorific stripping, modifier removal

**Topic marker preservation**:
Keeping Korean topic markers (은/는) when they are part of natural sentence flow. Removing them produces clipped, unnatural sentences.
_Avoid_: particle deletion

**Contrast connective preservation**:
Keeping contrast/concession adverbs (e.g. "다만", "하지만", "그런데") that carry logical flow between sentences. These are not AI signals — removing them breaks coherence.
_Avoid_: connective deletion

**Speech domain ending lock**:
In speech-domain text (YouTube, podcast, lecture, live), the sentence ending style (~해요체, ~합니다체, casual ~어/아) must never be changed — even when the ending looks fixable. This is enforced both in step 2 (pre-check) and step 5 (post-check).
_Avoid_: ending normalization, 다체 injection, speech-to-written conversion

**Reference post (참고 글)**:
A sample post provided by the user at the start of a session. The skill extracts tone patterns from it and applies them as a lightweight brand voice — without requiring a formal brand-voice file. Treated as a session-scoped Mode D.
_Avoid_: brand voice file, permanent profile, Mode E

## Relationships

- A **Third-party community demo** may use **korean-humanizer**, but it is not an **Official demo**.
- User input submitted to a **Third-party community demo** is handled by the external operator, not by this repository.

## Example Dialogue

> **Dev:** "Can we add the Socialistic link as the official demo?"
> **Domain expert:** "No. It can be listed as a **Third-party community demo**, but the README must say it is not an **Official demo** and that user input is processed by the external service."

## Flagged Ambiguities

- "demo" can mean either **Official demo** or **Third-party community demo**; resolved: Socialistic/Tinkerland is a **Third-party community demo**.
