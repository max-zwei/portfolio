/Users/max.pinkert/Documents/GitHub/portfolio/src/components/Avatar.astro
-> "max" has three variants, one with a shade of tomate as background and a tomato-500 body; one with a shade of herbs as background and herbs-500 as body; and one with a neutral background. They are currently in "Logo.astro", maybe we should move them here.

/Users/max.pinkert/Documents/GitHub/portfolio/src/components/BlankSection.astro
-> I did also use this as a default section for text paragraphs, so anywhere where I needed heading X plus body text. So would be a good idea to create a text-only section based on this section but more general. And then probably having the "BlankSection" as one variant of it.

/Users/max.pinkert/Documents/GitHub/portfolio/src/components/CvSection.astro
-> Where does "id?: string;" come from?
-> "/** Heading level appropriate to the page's document outline. */
  level?: 2 | 3 | 4;": It should always be the same heading level for all sections. I don't see the need to make this a variable. Heading 1 is "Experience" or "Education" as a wrapper for all experience or education related headings. And for the role I picked Body-Tall in Bold and for the company Body-Tall. Adjust also in the styling ".cv-section__company" and ".cv-section__role"

/Users/max.pinkert/Documents/GitHub/portfolio/src/components/FlipCard.astro
-> There is actually another transition I didnt define yet. The small variant should smoothly enlarge to the front state once hovering over it. And to make things even more complicated, the small cards will be in a packed collection and with hovering over them, they should bloat up. So the one in the hover focus enlarging to the front variant as I said but also the surrounding ones enlarging to suit the transition. As an example:
https://nothing-to-watch.port80.ch/?wt_mc=nl.red.tr.weeklybriefing.2025-08-22.link.link . The example is a bit too much, in the way that it has so much motion and transition, that the experience is very buggy and non-fluent.

/Users/max.pinkert/Documents/GitHub/portfolio/src/components/FocusAreas.astro
-> "/** Heading depth chosen by the page's document outline. */
  level?: 2 | 3 | 4;": Similar to CV sections, what is actually the purpose of having a variable for the level of heading?

/Users/max.pinkert/Documents/GitHub/portfolio/src/components/Logo.astro
-> Actually only for the favicon.svg, maybe we don't need the components here.

/Users/max.pinkert/Documents/GitHub/portfolio/src/components/NavBar.astro
-> Something that isnt visible yet, but actually the icons after "Explore with" will have a URL, so for example the chatgpt icon a link to "chat.openai.com/....".

/Users/max.pinkert/Documents/GitHub/portfolio/src/components/PostIt.astro
-> Add the following rotations for the four post it types with rotate(Ndeg):
herbs: 5°
tomato: -3°
lemon: 2°
pickled: -6°

Generally:
-> Review all components for correct token use
-> Review all components if they used existing components where relevant, e.g. the Button.astro in other components.
-> Where do Headings and Body Text Styles sit? 