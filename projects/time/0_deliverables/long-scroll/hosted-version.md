[time-scroll.netlify.app](https://time-scroll.netlify.app/)

## Local preview and deployment

From this directory, run `python3 -m http.server 4174` and open http://localhost:4174.
Upload this directory to the existing Netlify site's Deploys page to publish changes; editing these files does not update the hosted site automatically.

## Current design

- Matches Figma Mobile frame `233:1201`: Content starts at 1,125px, trends start 5,366px into Content, and each loop spans 18,686px at the 375px design width.
- Uses all 45 supplied named `_4x.webp` card exports and the fixed `assets/background.webp`. The Einstein meme (`233:1899`), absent from the supplied exports, is retained as `assets/cards/card-decades-13.png` exported from Figma.
- Card positions and dimensions live in `cards.json`; the loop height in `app.js` also controls the CSS aspect ratio. The introduction remains outside the loop.
- Artwork loads near the viewport, with two bounded copies for forward/reverse looping. Native headings and accessible image descriptions are retained.
- Verified in Chrome at 320, 375, 390, and 430px widths: all artwork loads, no horizontal overflow, repeated forward/reverse wrapping, and a touch swipe across the loop boundary. Physical-device Safari has not been verified.