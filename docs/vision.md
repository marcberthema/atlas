# Vision

Atlas is one website with the references needed in day-to-day work, so nobody has to dive into a product's documentation to look something
up. It is a place to look things up, not to ask questions. Each topic is a set of facts kept in JSON and generated into static pages, published at
atlas.marcberthelette.com. It is a personal project built with AI assistance, and everything in it comes from public sources.

## Audience

The author first, and anyone else who needs the same facts in one place. It is not an official resource of any product named in it.

## What a topic is

A topic collects what you need to look up about one subject: the workflow, the commands, the syntax, the options, the pitfalls, and the tools
around it. It summarises in short plain sentences, links the official page for each source, and shows official code examples fetched
unchanged. Every entry shows the version it was analysed against. Anything unverified says "unconfirmed".

## How it is organised

- **Two layers:** a family, then a topic. Families now: IaC, CI/CD, Development, Enterprise. CI/CD covers application delivery pipelines and the
  services around them (artifact repositories, scanners, quality gates).
- **A spec per topic:** `topics/<id>/docs/spec.md`, written before the content. Format: `docs/topic-spec.md`.
- **Adding a topic is a skill:** a command that reads the official documentation, writes the spec, then the entries, fetches the examples,
  validates, builds and commits to a branch for review. It never publishes on its own. A matching command refreshes a topic.

## Higher-level views

Generated from metadata on each topic, so a new topic appears in them without editing a diagram:

- **The DevOps loop:** the eight stages (plan, code, build, test, release, deploy, operate, monitor), each listing the topics that belong to it.
- **A typical IT estate on Azure:** areas such as identity, network, governance and workloads, showing where each tool fits.
- **A standard application:** web, API, data, messaging, identity and observability, showing where a service such as Kafka appears.

The estate and application views are generic and built from public reference architectures.

## Not goals

- Tutorials, Q&A, or opinions. Nothing is written from employer or client experience.
- Copying documentation. Atlas points to it.
- Paid products as subjects. A few appear as references so the reader knows they exist.
- A framework, a build service or external scripts. Python standard library, static pages that work from `file://`.
