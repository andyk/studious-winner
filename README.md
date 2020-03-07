# studious-winner

* virtualenv -p `which python3` studious-winner

## How a brain trains a policy

It's a spectrum between:

* Hardcoded by evolution
* Imitation learning
* Prior learnings for the world
* Direct Explorations

Concrete next step:

* Agent is in world
* Agent explores but learns nothing
* Agent explores and accumulates priors about the world

* Build out apple world to be an explorable space
    * layer of indirection between reward and action

* Build out agent ability to explore

* Once the world is explorable, you learn things:
    * to satisfy drives
    * just in case later tasks require early learnings


Mapping between agent <-> MDPs and policies.

Reward for satisfying hunger and explore drives (internal)


Andy parting ideas ->
1) Bayes -- building model, updating model
2) ExploreDrive - two different ways (explore broadly vs explore to satisfy drives)
3) sergey lecture on meta-RL
