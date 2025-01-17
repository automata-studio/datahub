from datahub.emitter.mce_builder import make_dataset_urn
from datahub.ingestion.source.state.kafka_state import KafkaCheckpointState


def test_kafka_common_state() -> None:
    state1 = KafkaCheckpointState()
    test_topic_urn = make_dataset_urn("kafka", "test_topic1", "test")
    state1.add_checkpoint_urn(type="topic", urn=test_topic_urn)

    state2 = KafkaCheckpointState()

    topic_urns_diff = list(
        state1.get_urns_not_in(type="topic", other_checkpoint_state=state2)
    )
    assert len(topic_urns_diff) == 1 and topic_urns_diff[0] == test_topic_urn


def test_kafka_state_migration() -> None:
    state = KafkaCheckpointState.parse_obj(
        {
            "encoded_topic_urns": [
                "kafka||test_topic1||test",
                "kafka||topic_2||DEV",
            ]
        }
    )
    assert state.urns == [
        "urn:li:dataset:(urn:li:dataPlatform:kafka,test_topic1,test)",
        "urn:li:dataset:(urn:li:dataPlatform:kafka,topic_2,DEV)",
    ]
