# Controls, states and motion

Read this for forms, menus, state changes and keyboard or touch behavior. Preserve the product's working interactions while changing its appearance.

Use the native element for the action: a link for navigation, a button for an action, and a labeled input for a value. Associate visible labels programmatically. Give icon-only actions meaningful accessible names. Support keyboard operation and visible focus. Opacity and `pointer-events: none` alone do not disable a control for every input method.

Keep touch actions available without hover. WCAG 2.2 AA target size is generally at least 24 by 24 CSS pixels, subject to its spacing and other exceptions. A larger target often improves touch use. Treat a recipe's 12px glyph or dot as its visual size, not its full hit area. [W3C target-size guidance](https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum.html)

## State and recovery

Distinguish initial, loading, successful, empty, unavailable and failed states. Report actual progress when measured; use an honest indeterminate state otherwise. A successful request is not always a persisted result. Confirm the operation at the level the message claims.

Keep user input through recoverable errors. Explain what happened and the useful next action. Persistent failures need persistent recovery controls. Use optimistic updates for operations that can be reversed and recovered. Prevent competing writes when they would corrupt the result.

Match asynchronous results to the current target and request. Navigation, replacement input or cancellation can make an old result stale. A reconnect alone does not establish that the displayed result is current.

## Menus, dialogs and editing

Manage focus when opening and closing overlays. Closed content must leave the keyboard path when appropriate; clipping it visually is insufficient. Keep Escape behavior consistent with the interaction and preserve unsaved work according to the product's established policy.

Respect framework ownership of rendered nodes. A higher z-index cannot escape a native modal's top layer and inertness rules. Tool overlays that must work inside a modal need the correct host and focus behavior.

For inline editing, preserve mixed content and data types. Enter that commits an IME candidate must not submit the form. Avoid unexpected autofocus that opens a phone keyboard.

## Motion

Use motion to explain continuity, placement or state. Match its duration to the distance and task. Support interruption and remove listeners or scheduled work when the interaction ends.

Provide a reduced-motion state that retains the content and meaning. Keep essential information available without waiting for an entrance animation. A count-up is inappropriate for a live operational value. Pause continuing decorative motion when needed, and preserve native scrolling and reachable controls through any scroll-linked sequence.
