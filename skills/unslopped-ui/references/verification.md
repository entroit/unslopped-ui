# Verify the claimed result

Read this before reporting completion of a visual or functional change. Use the project's available checks and rendered application. Scale verification to the changed behavior.

## Visual evidence

Capture or inspect the result after the final source, font and asset changes. Wait for the intended fonts and images to load. Check a representative wide view, a narrow view and any intermediate width where the layout changes. Inspect the actual states affected by the edit, including content extremes where they matter.

Review reading order, hierarchy, clipping, overlap, wrapping and background-dependent contrast. Compare the change with the brief and existing system. A screenshot proves the captured state and viewport; it does not prove all breakpoints or interactions.

Check zoom and reflow when the change affects layout or text. WCAG reflow commonly uses a 320 CSS-pixel-wide viewport, equivalent to a 1280px viewport at 400% zoom, with exceptions for content that requires two-dimensional layout. Text resize at 200% is a separate check. [W3C reflow guidance](https://www.w3.org/WAI/WCAG21/Understanding/reflow.html)

## Behavior

Exercise the affected action through its normal user path. Check keyboard focus and operation for changed controls. For touch or dragging, test the actual gesture, scrolling across the target and cancellation when those behaviors matter. Resizing the viewport alone does not test touch.

Verify success, failure and recovery at the level the UI claims. Check computed totals against their data and definitions. A static success toast cannot establish persistence; a direct scripted click may bypass occlusion or inertness. Note the distinction when the environment permits only a limited check.

## Scanner evidence

Record the tool, scope and actual outcome. Distinguish not run, unavailable, failed, partial, complete with findings and complete without findings. An empty result from a static scan does not prove rendered accessibility or design quality.

Inspect each finding's context before repairing it. A source rule may be an aesthetic preference, a conservative heuristic or an actual functional defect. A deliberate brand choice can justify a style exception. Missing focus, unreadable required text and fabricated data still need correction.

Scope waivers narrowly and retain their reason. Do not change semantics or hide content merely to evade a detector. If a screenshot or source changes during verification, repeat the affected check against the final artifact.

## Report

State the concrete changes, checks performed and remaining gaps. Name whether the evidence came from rendered inspection, a user interaction, a source check or a test. Do not convert an inaccessible environment or a skipped check into a pass.
