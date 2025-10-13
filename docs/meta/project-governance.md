# Project Governance

This document describes how the pdfly project is managed. It describes the
different actors, their roles, and the responsibilities they have.

## Terminology

* The **project** is pdfly - a free and open-source pure-python PDF command line
tool.
  It includes the [code, issues, and discussions on GitHub](https://github.com/py-pdf/pdfly),
  and [the documentation on ReadTheDocs](https://pdfly.readthedocs.io/en/latest/),
  [the package on PyPI](https://pypi.org/project/pdfly/).
* A **maintainer** is a person who has technical permissions to change one or
  more part of the projects. It is a person who is driven to keep the project running
  and improving.
* A **contributor** is a person who contributes to the project. That could be
  through writing code - in the best case through forking and creating a pull
  request, but that is up to the maintainer. Other contributors describe issues,
  help to ask questions on existing issues to make them easier to answer,
  participate in discussions, and help to improve the documentation. Contributors
  are similar to maintainers, but without technical permissions.
* A **user** is a person who imports pdfly into their code. All pdfly users
  are developers, but not developers who know the internals of pdfly. They only
  use the public interface of pdfly. They will likely have less knowledge about
  PDF than contributors.
* The **community** is all of that - the users, the contributors, and the maintainers.


## Governance, Leadership, and Steering pdfly forward

pdfly is a free and open source project.

As pdfly does not have any formal relationship with any company and no funding,
all the work done by the community are voluntary contributions. People don't
get paid, but choose to spend their free time to create software of which
many more are profiting. This has to be honored and respected.

pdfly has the **Benevolent Dictator**
governance model. The benevolent dictator is a maintainer with all technical permissions -
most importantly the permission to push new pdfly versions on PyPI.

Being benevolent, the benevolent dictator listens for decisions to the community and tries
their best to make decisions from which the overall community profits - the
current one and the potential future one. Being a dictator, the benevolent dictator always has
the power and the right to make decisions on their own - also against some
members of the community.

As pdfly is free software, parts of the community can split off (fork the code)
and create a new community. This should limit the harm a bad benevolent dictator can do.


## Project Language

The project language is (american) English. All documentation and issues must
be written in English to ensure that the community can understand it.

We appreciate the fact that large parts of the community don't have English
as their mother tongue. We try our best to understand others -
[automatic translators](https://translate.google.com/) might help.


## Expectations

The community can expect the following:

* The **benevolent dictator** tries their best to make decisions from which the overall
  community profits. The benevolent dictator is aware that his/her decisions can shape the
  overall community. Once the benevolent dictator notices that she/he doesn't have the time
  to advance pdfly, he/she looks for a new benevolent dictator. As it is expected
  that the benevolent dictator will step down at some point of their choice
  (hopefully before their death), it is NOT a benevolent dictator for life
  (BDFL).
* Every **maintainer** (including the benevolent dictator) is aware of their permissions and
  the harm they could do. They value security and ensure that the project is
  not harmed. They give their technical permissions back if they don't need them
  any longer. Any long-time contributor can become a maintainer. Maintainers
  can - and should! - step down from their role when they realize that they
  can no longer commit that time.
* Every **contributor** is aware that the time of maintainers and the benevolent dictator is
  limited. Short pull requests that briefly describe the solved issue and have
  a unit test have a higher chance to get merged soon - simply because it's
  easier for maintainers to see that the contribution will not harm the overall
  project. Their contributions are documented in the git history and in the
  public issues.
* Every **community member** uses a respectful language. We are all human, we
  get upset about things we care and other things than what's visible on the
  internet go on in our live. pdfly does not pay its contributors - keep all
  of that in mind when you interact with others. We are here because we want to
  help others.


### Issues and Discussions

An issue is any technical description that aims at bringing pdfly forward:

* Bugs tickets: Something went wrong because pdfly developers made a mistake.
* Feature requests: pdfly does not support all features of the PDF specifications.
  There are certainly also convenience methods that would help users a lot.
* Robustness requests: There are many broken PDFs around. In some cases, we can
  deal with that. It's kind of a mixture between a bug ticket and a feature
  request.
* Performance tickets: pdfly could be faster - let us know about your specific
  scenario.

Any comment that is in those technical descriptions which is not helping the
discussion can be deleted. This is especially true for "me too" comments on bugs
or "bump" comments for desired features. People can express this with 👍 / 👎
reactions.

[Discussions](https://github.com/py-pdf/pdfly/discussions) are open. No comments
will be deleted there - except if they are clearly unrelated spam or only
try to insult people (luckily, the community was very respectful so far 🤞)


### Releases

The maintainers follow [semantic versioning](https://semver.org/). Most
importantly, that means that breaking changes will have a major version bump.

Be aware that unintentional breaking changes might still happen. The `pdfly`
maintainers do their best to fix that in a timely manner - please
[report such issues](https://github.com/py-pdf/pdfly/issues)!


## People

* Martin Thoma is benevolent dictator since April 2022.
* Maintainers:
    * Matthew Stamy (mstamy2) was the benevolent dictator for a long time.
      He still is around on GitHub once in a while and has permissions on PyPI and GitHub.
    * Matthew Peveler (MasterOdin) is a maintainer on GitHub.
