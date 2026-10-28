# Visual details

Read this when changing type, color, spacing or component styling. Use the product's existing tokens first. Add a new value when it expresses a real role that the existing system cannot cover.

## Typography

Choose faces for their role, available glyphs and fit to the identity. Inter and system fonts can be appropriate. A different font does not repair weak hierarchy.

Establish a visible difference between heading, body, supporting text and data. Judge the actual words at the intended size and width. Short display text can use tighter leading than prose; long headings and dense body text need room for their glyphs and lines. Inspect clipping, awkward breaks, excessive tracking and isolated final words with the actual loaded font.

Use casing for meaning and identity. Keep functional labels easy to recognize. A brand's uppercase navigation is not a reason to turn paragraphs into tracked capitals. Use a monospace face when fixed widths, code or the selected identity need it.

## Color and contrast

Give colors roles: ground, content, boundary, action and state. Apply the action color selectively enough that the next step remains identifiable. A dark inset well and a lighter elevated panel express different relationships; neither is a universal rule for every dark-mode component.

Measure contrast on the actual painted background, including opacity, imagery, gradients and overlays. WCAG AA generally requires 4.5:1 for ordinary text and 3:1 for large text. Large text is at least 24 CSS pixels, or about 18.67 CSS pixels when bold. Applicable control boundaries and meaningful graphics generally need 3:1. Account for the standard's actual exceptions; faint readable content is not automatically disabled content. [W3C contrast guidance](https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html)

A gradient's best passing stop does not prove that all glyphs pass. Inspect the relevant locations. Preserve readable status text and focus indicators across normal, hover, selected, disabled and error states. Use more than color to carry essential distinctions.

## Spacing and shape

Use consistent edges and a small spacing vocabulary. Put related items closer than unrelated groups. Choose content-driven breakpoints and check intermediate widths; a desktop and phone screenshot alone can miss the failure between them.

Choose radius, border and shadow according to grouping, containment and elevation. Nested radii should follow the geometry, with an inner radius near `max(0, outer radius - inset)` when the curves are concentric. Inspect unequal borders and padding rather than applying that formula blindly.

Keep component dimensions appropriate to their content and input method. Dense app rows and spacious marketing sections have different jobs. A larger visual button is not useful if its label is vague; a tiny icon can retain its appearance inside a larger hit target.

## Effects

Keep an effect when it supports identity or explains a change. Assess its cost, readability and behavior on the actual device. Decorative texture, blur and shadow must not hide content or become evidence of quality by themselves. Apply motion rules from the interaction reference when an effect moves.
