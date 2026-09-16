#import "@preview/cetz:0.3.4"

#set page(width: 21cm, height: 6.7cm, margin: 0.15cm, fill: none)
#set text(font: "DejaVu Sans", size: 9.5pt, fill: rgb("#222222"))

#cetz.canvas(length: 1cm, {
  import cetz.draw: *

  let ink = rgb("#333333")
  let muted = rgb("#666666")
  let accent = rgb("#326899")
  let quiet = (paint: muted, thickness: 0.6pt)
  let axis-y = 2.85
  let source-x = 1.05
  let detector-x = 18.75
  let sample-xs = (5.6, 7.1, 8.6, 10.1)
  let positions = (156, 158, 166, 187)

  // Sequential acquisitions; positions are spread for legibility, not to scale.
  line((source-x, axis-y), (20.0, axis-y), stroke: quiet,
    mark: (end: "stealth", fill: muted, scale: 0.7), name: "axis")
  content("axis.end", anchor: "west", [$z$])

  line((source-x, axis-y), (detector-x, 4.8), stroke: quiet)
  line((source-x, axis-y), (detector-x, 0.9), stroke: quiet)
  circle((source-x, axis-y), radius: 0.075, fill: ink, stroke: none, name: "source")
  content((source-x, 4.2), align(center)[Waveguide\ point source], anchor: "south")

  for (index, x) in sample-xs.enumerate() {
    let selected = index == 0
    let color = if selected { accent } else { muted }
    line((x, 1.50), (x, 4.20),
      stroke: (paint: color, thickness: if selected { 1.8pt } else { 1pt },
        dash: if selected { "solid" } else { "dashed" }),
      name: "sample-" + str(index + 1))
    content((x, 4.42), [$j = #(index + 1)$], anchor: "south")
    content((x, 1.28), [#positions.at(index)], anchor: "north")
  }
  content((7.85, 5.42), [Same sample at four successive positions], anchor: "south")
  line((5.6, 5.10), (10.1, 5.10), stroke: quiet,
    mark: (end: "stealth", fill: muted, scale: 0.7))
  content((7.85, 0.63), [Source–sample distance (mm)], anchor: "north")

  line((detector-x, 0.9), (detector-x, 4.8),
    stroke: (paint: ink, thickness: 2pt), name: "detector")
  content("detector.end", [Fixed detector], anchor: "south", padding: 0.16cm)
  content((15.3, 3.65), [Record $y_j$ at each position], anchor: "south")

  // One acquisition's two physical path lengths, j=1 highlighted above.
  line((source-x, 0.03), (sample-xs.first(), 0.03), stroke: quiet,
    mark: (start: "|", end: "|", scale: 0.65))
  content(((source-x + sample-xs.first()) / 2, -0.1), [$R_(1,j)$], anchor: "north")
  line((sample-xs.first(), 0.03), (detector-x, 0.03), stroke: quiet,
    mark: (start: "|", end: "|", scale: 0.65))
  content(((sample-xs.first() + detector-x) / 2, -0.1), [$R_(2,j)$], anchor: "north")
  content((15.3, 5.42), [Source–detector: 5.178 m], anchor: "south")
})
