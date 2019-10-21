# Physics research
Though I am well-versed in most subfields of physics, my specific research focus is on "astroparticle physics"; a melding of quantum field theory (QFT) and particle physics, conventional astrophysics, and physical cosmology. This area of research concerns itself with questions involving the conditions of the early universe (fractions of a second after the Big Bang), [dark matter](https://en.wikipedia.org/wiki/Dark_matter), [dark energy](https://en.wikipedia.org/wiki/Dark_energy), and in general, any scenario where elementary particle physics can shed light on astrophysical or cosmological phenomena.

## Condensates
Within this subfield, my expertise lies mainly in the study of "condensates" - quantum fluids that form under unusual conditions (very cold temperatures, high densities, strong attractive forces, etc.), causing all the particles in the fluid to "synchronize" in their ground state. Though the specific types of condensates that I typically study ($Q$-balls, boson stars, axion miniclusters) are still hypothetical, condensates are very much real! In 2001, Cornell, Ketterle and Wieman shared the [Nobel Prize in physics](https://www.nobelprize.org/prizes/physics/2001/summary/) for their groundbreaking work in producing a _Bose-Einstein_ condensate in a laboratory, which was created using Rubidium atoms supercooled to 20 nK (20 billionths of a degree from absolute zero). The only difference really is that I am interested in condensates made from exotic, undiscovered types of matter, with (even more) unusual properties!

These condensates are very interesting from a cosmological perspective because:

* some of them have just the right properties to make them good potential dark matter candidates
    * lack of interaction with regular light and matter
    * small, but nonzero self-interactions
* the conditions in the early universe were probably _just right_ to produce them
    * very high densities shortly after the Big Bang
    * the occurence of [spontaneous symmetry breaking](https://en.wikipedia.org/wiki/Spontaneous_symmetry_breaking)
    * it would be near impossible to create one in a lab today (remember, these are not the same kind as the ones that _were_ made in 2001)
* they could be responsible for creating primordial black holes (PBH) by clustering together shortly after being created
    * could then lead to PBH being dark matter!
    * less fine-tuning than inflation-inspired models

## Solitons
The most interesting thing about condensates (in my opinion) is that they can form solitons! What is a soliton? A [soliton](https://en.wikipedia.org/wiki/Soliton), in the simplest possible definition, is an object that can form a stable, localized structure, and does not dissapate over a significant length of time. Under this definition, you might consider a star, baseball, or even a cat as as soliton because they are localized and maintain their shapes for long periods. A puff of air, or a wave on the ocean are not solitons because they have no stable form, and will quickly disperse after a short time.

Condensates typically form solitons that are similar in nature to water droplets. They have a fluid nature, and an attractive short-range self-interaction that leads to a surface tension which can keep the soliton from breaking apart or dissapating. The simplest condensate solitons can be described through a scalar field theory with a global $U(1)$ symmetry of the form
$$\mathcal{L} = \frac{1}{2} \partial_\mu \phi^\dagger \partial^\mu \phi - V(\phi)$$
where $V(\phi) = \tfrac{1}{2} m^2 |\phi|^2 - \lambda |\phi|^4 + (\gamma/m^2) |\phi|^6$ is an "attractive" potential, i.e. $\exists \phi_*$ such that $V(\phi_*) \lt \frac{1}{2} m^2 |\phi_*|^2$ meaning that $\phi$ finds it more energetically favorable to reside in the condensate state rather than exist as a free particle.

# My contributions

## Papers
I have authored a variety of papers on the subject (most with the help of my brilliant collaborators), which can be found through paper aggregators such as [arXiv](https://arxiv.org/search/astro-ph?searchtype=author&query=Cotner%2C+E) (free preprints), [Google Scholar](https://scholar.google.com/citations?user=sERkI8cAAAAJ&hl=en&oi=ao) (peer-reviewed journals, potentially behind a paywall), and [InspireHEP](http://inspirehep.net/search?ln=en&p=a+cotner&of=hb&action_search=Search&sf=earliestdate&so=d) (basically same as arXiv). You can find my PhD dissertation indexed at the University of California's [eScholarship repository](https://escholarship.org/uc/item/8kt7j20g). If you would like to collaborate, please <a href="{{ url_for('about') }}">reach out</a>!

## Conferences
I have been an invited speaker at several conferences to share my work with the physics community. In reverse chronological order:

* [PACIFIC 2018](https://conferences.pa.ucla.edu/pacific-2018/) - Kiroro, Hokkaido, Japan
* [PBH Focus Week](https://indico.ipmu.jp/indico/event/138/contributions/676/), Univ. of Tokyo IPMU, Chiba, Japan
* [PACIFIC 2016](https://conferences.pa.ucla.edu/pacific2016/) - Gump Station, Mo'orea, French Polynesia

## Code
Due to the theoretical nature of my studies, a lot of my work is computational in nature. You can find the code for some of the simulations I've run in [this GitHub repo](https://github.com/ecotner/physics-research). Warning: it's messy (wrote most of it before I learned proper coding discipline). Below are some simulations of gravitationally-interacting condensates I have produced:

<center>
<!-- <img src="https://i.imgur.com/k1XpnxO.gif" alt="2d boson stars orbiting each other" style="vertical-align: middle; margin-right: 5%;">
<img src="https://i.imgur.com/OMC82pl.gif" alt="3d merger of attractive boson stars" style="vertical-align: middle;"> -->
<blockquote class="imgur-embed-pub" lang="en" data-id="a/WLmAJjZ"><a href="//imgur.com/a/WLmAJjZ">View post on imgur.com</a></blockquote><script async src="//s.imgur.com/min/embed.js" charset="utf-8"></script>
</center>
