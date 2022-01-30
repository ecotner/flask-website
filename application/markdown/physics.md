# Physics research
Though I am well-versed in most sub-fields of physics, my specific research focus is on "astroparticle physics"; a melding of quantum field theory (QFT) and particle physics, conventional astrophysics, and physical cosmology. This area of research concerns itself with questions involving the conditions of the early universe (fractions of a second after the Big Bang), [dark matter](https://en.wikipedia.org/wiki/Dark_matter), [dark energy](https://en.wikipedia.org/wiki/Dark_energy), and in general, any scenario where elementary particle physics can shed light on astrophysical or cosmological phenomena.

## Condensates
Within this sub-field, my expertise lies mainly in the study of ["condensates"](https://en.wikipedia.org/wiki/Bose%E2%80%93Einstein_condensate) - quantum fluids that form under unusual conditions (very cold temperatures, high densities, strong attractive forces, etc.), causing all the particles in the fluid to "synchronize" in their ground state. Though the specific types of condensates that I typically study (Q-balls, boson stars, axion miniclusters) are still hypothetical, condensates are very much real! In 2001, Cornell, Ketterle and Wieman shared the [Nobel Prize in physics](https://www.nobelprize.org/prizes/physics/2001/summary/) for their groundbreaking work in producing a _Bose-Einstein_ condensate in a laboratory, which was created using Rubidium atoms supercooled to 20 nK (20 billionths of a degree from absolute zero). The only difference really is that I am interested in condensates made from exotic, undiscovered types of matter, with (even more) unusual properties!

These condensates are very interesting from a cosmological perspective because:

* some of them have just the right properties to make them good potential dark matter candidates
    * lack of interaction with regular light and matter
    * small, but nonzero self-interactions
* the conditions in the early universe were probably _just right_ to produce them
    * very high densities shortly after the Big Bang
    * the occurrence of [spontaneous symmetry breaking](https://en.wikipedia.org/wiki/Spontaneous_symmetry_breaking)
    * it would be near impossible to create one in a lab today (remember, these are not the same kind as the ones that _were_ made in 2001)
* they could be responsible for creating primordial black holes (PBH) by clustering together shortly after being created
    * could then lead to PBH being dark matter!
    * less fine-tuning than inflation-inspired models

## Solitons
The most interesting thing about condensates (in my opinion) is that they can form solitons! What is a soliton? A [soliton](https://en.wikipedia.org/wiki/Soliton), in the simplest possible definition, is an object that can form a stable, localized structure, and does not dissipate over a significant length of time. Under this definition, you might consider a star, baseball, or even a cat as as soliton because they are localized and maintain their shapes for long periods. A puff of air, or a wave on the ocean are not solitons because they have no stable form, and will quickly disperse after a short time.

Condensates typically form solitons that are similar in nature to water droplets. They have a fluid nature, and an attractive short-range self-interaction that leads to a surface tension which can keep the soliton from breaking apart or dissipating. The simplest condensate solitons can be described through a scalar field theory with a global $U(1)$ symmetry of the form
$$\mathcal{L} = \frac{1}{2} \partial_\mu \phi^\dagger \partial^\mu \phi - V(\phi)$$
where $V(\phi) = \tfrac{1}{2} m^2 |\phi|^2 - \lambda |\phi|^4 + (\gamma/m^2) |\phi|^6$ is an "attractive" potential, i.e. $\exists \phi_*$ such that $V(\phi_*) \lt \frac{1}{2} m^2 |\phi_*|^2$ meaning that $\phi$ finds it more energetically favorable to reside in the condensate state rather than exist as a free particle when the field takes on a classical value near $\phi=\phi_*$.

## Primordial black holes
Another dark matter candidate that I have studied are known as ["primordial" black holes](https://en.wikipedia.org/wiki/Primordial_black_hole) (PBH). PBH are hypothetical black holes that could have been created in the early universe from large density fluctuations, fractions of a second after the Big Bang. Typically, astrophysical black holes are created when a star cannot support its own weight anymore, and collapses under its own gravity.

The two types of black holes are are created at different times and in different ways, which means that they can have drastically different masses. Because regular black holes form from stars, their mass cannot be less than the mass of the star it was formed from, which means that all regular black holes must have masses greater than about one solar mass (the mass of our Sun). Primordial black holes, on the other hand, have no such restriction, and can form with pretty much any mass, ranging from as small as the Planck mass (22 μg; about the mass of a flea), to tens of thousands of solar masses.

As a general rule of thumb, the mass of a PBH is roughly the same as the mass of the cosmological horizon in which it formed. This means that there is a relationship between the PBH mass $M$ and the cosmological time (age of the universe) of formation $t$ of the form
$$M \sim \rho_c \lambda_\text{hor}^3 \sim \left(\frac{1}{6\pi G t^2}\right) (ct)^3 = \frac{c^3 t}{6\pi G},$$
where $\rho_c = 3H^2/8\pi G$ and $\lambda_\text{hor}$ are the "critical density" and horizon size of the universe, and I have used very rough estimates such as $H \sim 2/3t$ and $\lambda_\text{hor} \sim ct$. Since the PBH mass is proportional to $t$, if the black holes are formed very early, then they are very "small" ($t=10^{-12}$ sec $\rightarrow$ $M$ is about the mass of the moon). If they are formed later, they can be very large ($t = 1$ sec $\rightarrow$ $M \approx 10,000$ solar masses).

Since PBH are created much earlier than normal BH, they have plenty more time to cluster together and merge, which means they could form the seeds of the *supermassive* (millions and billions of solar masses) black holes we see in nuclei of galaxies today. There are observational constraints (e.g. gravitational lensing from when a PBH passes in front of a star) that rule out part of the mass range, but they haven't been completely ruled out yet.

Part of my work was in the proposition of a mechanism by which PBH could have been produced in the early universe. The basic idea is that since condensate solitons could be easily produced in the early universe, maybe in some regions of space they could cluster together and collapse into a black hole during a matter-dominated epoch. It turns out that it is much easier to create PBH through this mechanism than some of the other proposed theories, which involve a high degree of fine-tuning. One reason for this is that density fluctuations in a matter-dominated era are not suppressed as much as fluctuations in a radiation-dominated era. Another reason is that because the number of solitons formed per horizon (roughly between $10^4 - 10^9$) is significantly smaller than the typical number of elementary particles per horizon, the RMS density fluctuations (which go like $\sigma \sim N^{-1/2}$) are greatly enhanced.

Read more about [my work](https://arxiv.org/abs/1612.02529) [here](http://newsroom.ucla.edu/releases/ucla-physicists-propose-new-theories-of-black-holes-from-the-very-early-universe).

# My contributions to the field

## Publications
I have authored a variety of papers on the subject (most with the help of my brilliant collaborators), which can be found through paper aggregators such as [arXiv](https://arxiv.org/search/astro-ph?searchtype=author&query=Cotner%2C+E) (free preprints), [Google Scholar](https://scholar.google.com/citations?user=sERkI8cAAAAJ&hl=en&oi=ao) (peer-reviewed journals, potentially behind a paywall), and [InspireHEP](http://inspirehep.net/search?ln=en&p=a+cotner&of=hb&action_search=Search&sf=earliestdate&so=d) (basically same as arXiv). You can find my PhD dissertation indexed at the University of California's [eScholarship repository](https://escholarship.org/uc/item/8kt7j20g). If you would like to collaborate, please <a href="{{ url_for('about') }}">reach out</a>!

## Conferences
I have been an invited speaker at several conferences to share my work with the physics community. In reverse chronological order:

* [PACIFIC 2018](https://conferences.pa.ucla.edu/pacific-2018/) - Kiroro, Hokkaido, Japan
* [PBH Focus Week](https://indico.ipmu.jp/indico/event/138/), Univ. of Tokyo IPMU, Chiba, Japan
* [PACIFIC 2016](https://conferences.pa.ucla.edu/pacific2016/) - Gump Station, Mo'orea, French Polynesia

## Code
Due to the theoretical nature of my studies, a lot of my work is computational in nature. You can find the code for some of the simulations I've run in [this GitHub repo](https://github.com/ecotner/physics-research). Warning: it's messy (wrote most of it before I learned proper coding discipline). Below are some simulations of gravitationally-interacting condensates I produced as part of a research project on the [scattering properties of boson stars](https://arxiv.org/abs/1608.00547):

<center>
<blockquote class="imgur-embed-pub" lang="en" data-id="a/WLmAJjZ"><a href="//imgur.com/a/WLmAJjZ"></a></blockquote><script async src="//s.imgur.com/min/embed.js" charset="utf-8"></script>
</center>

# Education and volunteer work

## Teaching
In theoretical research, funding is usually pretty tight (experimentalists get all the big bucks to make/maintain their experiments), so during my graduate degree, I taught undergraduate classes pretty much every quarter, including summers.
Some people hate it and would rather just do research full time, but I found it to be an extremely rewarding experience.
I taught both lecture and laboratory classes as a Teaching Assistant/Fellow for class sizes spanning 10 to 150 students, and difficulty levels ranging from introductory mechanics for biology and pre-med students to advanced nuclear/particle/cosmology classes for upper-division physics majors (electromagnetism was my "specialty" - I taught that one like 6 times at varying levels).
I was awarded the Outstanding TA Award in 2014 for exceptional student reviews, but I have always had great reviews every quarter (they only let you win it once 😉).

My teaching style is kind of like storytelling - I never try to just hand-wave something if it can be helped, and after explaining a problem/concept, I'll take a step back and try and contextualize it in terms of the overall goal/idea so that there's a reason for every step. I especially enjoyed working out problems on the blackboard/whiteboard; I'd always try and make it as far as I could without having to reference my notes, which kept me sharp and on my toes, reinforced my fundamentals, and I'm sure it impressed the students too :3

## Community outreach
While studying and teaching can be time consuming, I have also found a bit of time to volunteer my time for community outreach. Every year from 2014 - 2017 I have been a volunteer for UCLA's [Exploring Your Universe](https://www.exploringyouruniverse.org/) program. EYU is a an "open house" event where the all the departments in the physical sciences open their doors to the public to stage scientific demonstrations and lectures all across campus. Every year, I trained a group of O(10) undergraduate students how to operate equipment and demonstrate it to the public.

I also played a very minor role in the 2017 [APS Conference for Undergraduate Women in Physics](https://conferences.pa.ucla.edu/cuwip-ucla/index.html), where I advised interested undergraduates on what to expect from graduate school, and helped organize some of the social events.
