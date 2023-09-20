import random


class SomeModel:
    def predict(self, message: str) -> float:
        return random.uniform(0.0, 1.0)


def predict_message_mood(
    message: str,
    model: SomeModel,
    bad_thresholds: float = 0.3,
    good_thresholds: float = 0.8,
) -> str:
    if bad_thresholds > good_thresholds:
        raise ValueError("Incorrect values of tresholds")
    prediction = model.predict(message)
    if prediction < bad_thresholds:
        return "неуд"
    if prediction > good_thresholds:
        return "отл"
    return "норм"
