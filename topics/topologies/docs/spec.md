# Enterprise topologies: spec

Status: published (Enterprise family). Data checked 2026-10-26. Reconstructed from the data and git history, not written before the content:
reasons that the history does not record are marked "reason unconfirmed". Format: `docs/topic-spec.md`.

## Purpose and audience

How systems talk to each other: hub-and-spoke, mesh, tree, bus and ring, where each shows up in networks, services, messaging and data, and the
products that implement them. For someone drawing or reviewing an architecture who needs the shape, its trade-offs and where it appears.

## Scope

- In: the shapes, and the products and standards where they are most visible (service meshes, message buses, DNS, Cassandra, Prometheus
  federation). Open source tools are tracked with versions. The Azure and AWS network services are references, marked not open source.
- Out: step-by-step product setup (the product topics cover that). A reference design is never called a standard unless a source does.

## Layout

Archetype: concepts. Eight tabs: Hub-and-spoke, Mesh, Hierarchical (tree), Bus, Ring (the five shapes), Other topologies and products,
Compare, and Standard topologies (a group tab showing every entry of the `reference` group in full). Groups: topologies, networks and naming,
service-to-service and messaging, data and monitoring, standard topologies. Comparisons: the topologies side by side, message buses, service
meshes. Entries have diagrams drawn from a spec as inline SVG.

## Sources

Vendor and project documentation: the Azure hub-spoke and landing zone pages, the AWS Transit Gateway guide, Istio and Linkerd docs, Kafka,
RabbitMQ and NATS docs, the Cassandra and Prometheus docs, and RFC 1034 for DNS. The shapes are read "as of 2026-10-26". Re-check with
`make topologies-check` and re-read the pages in each entry's `sources`.

## Coverage

| Item | Status | Notes |
|---|---|---|
| `hub-and-spoke` | done | |
| `mesh` | done | |
| `tree` | done | |
| `bus` | done | |
| `ring` | done | |
| `point-to-point` | done | overview |
| `hybrid` | done | overview |
| `azure-hub-spoke` | done | cloud reference, no `track` |
| `aws-transit-gateway` | done | cloud reference, no `track` |
| `dns` | done | RFC 1034 |
| `istio` | done | |
| `linkerd` | done | |
| `kafka` | done | no `track` |
| `rabbitmq` | done | |
| `nats` | done | |
| `cassandra` | done | no `track` |
| `prometheus` | done | |
| `ref-landing-zone` | done | reference design |
| `ref-multi-region` | done | reference design |
| `ref-hybrid` | done | reference design |
| `ref-aws-transit` | done | reference design |
| `ref-multicluster-gitops` | done | reference design |
| `ref-mesh` | done | reference design |
| `ref-event-backbone` | done | reference design |
| `ref-metrics` | done | reference design |
| `ref-dns` | done | reference design |

## Known gaps

- Start dates: 25 of 26 entries are `started` unconfirmed.
- Four entries have no `track` (the two cloud references, Kafka and Cassandra), so the update check skips them. Whether Kafka and Cassandra
  have a release feed the checker can use is not recorded: reason unconfirmed.
- The standard topologies are reference designs taken from vendor or project docs, not standards: each says whose docs it comes from.

## Decisions

- Cloud network services are included as references because the shapes are most visible there, and are marked not open source.
- The Standard topologies tab is a group tab (every entry of the group in full). Reason: the reference designs are meant to be read together.
- The Kafka entry here is the messaging shape, not a Kafka reference: a Kafka topic would be a separate entry. The application view in the
  roadmap would place Kafka in a messaging area.

## Updating

Run `make topologies-check` after a release of Istio, Linkerd, Kafka, RabbitMQ, NATS or Prometheus, re-read the pages in `sources`, then update
`version`, the facts and `checked` together. Check each diagram in a browser after editing it.
