from __future__ import annotations

from groundpulse_agent.firestore_repo import FirestoreRunRepository
from groundpulse_agent.p1_models import ResearchRequest, transition_run


PROJECT_ID = "gen-lang-client-0100610229"


def make_request() -> ResearchRequest:
    return ResearchRequest.model_validate(
        {
            "idempotency_key": "firestore-roundtrip-001",
            "question": (
                "Given one approved CelesTrak GP snapshot for the ISS, "
                "what is source-backed and what is unavailable?"
            ),
            "decision_intent": "Firestore repository connectivity test",
            "object": {
                "name": "ISS",
                "norad_catalog_id": "25544",
            },
            "allowed_source_ids": ["celestrak_gp_25544"],
            "authorization_state": "approved_public_source",
            "non_claims": ["No live telemetry"],
        }
    )


def main() -> None:
    repository = FirestoreRunRepository(project=PROJECT_ID)
    created = repository.create(make_request())
    run_id = created.run_id

    try:
        queued = transition_run(created, "queued")
        repository.save(queued)

        recovered = repository.get(run_id)

        if recovered is None:
            raise RuntimeError("Firestore returned no document after save")

        if recovered.run_id != run_id:
            raise RuntimeError("Recovered run_id does not match created run_id")

        if recovered.status != "queued":
            raise RuntimeError(
                f"Expected queued status, got {recovered.status}"
            )

        if recovered.request.idempotency_key != "firestore-roundtrip-001":
            raise RuntimeError("Idempotency key did not round-trip correctly")

        print("Firestore round trip passed")
        print("Project:", PROJECT_ID)
        print("Collection:", repository.collection)
        print("Run ID:", recovered.run_id)
        print("Status:", recovered.status)
        print("Object:", recovered.request.object.name)
        print("Idempotency key:", recovered.request.idempotency_key)

    finally:
        repository._document(run_id).delete()
        print("Temporary Firestore document deleted")


if __name__ == "__main__":
    main()
