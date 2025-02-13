from fastapi import APIRouter, status
from pydantic import BaseModel, Field
import numpy as np
import onnxruntime as rt
from pathlib import Path

router = APIRouter(prefix="/v1")


class Inference(BaseModel):
    """Everything field you define here will be inherited by InferenceIn and InferenceOut."""

    pass


class InferenceIn(Inference):
    """The features of your dataset needed to perform inference.

    This example here is for the Iris dataset.
    """

    sepal_length: float = Field(ge=0.0)
    sepal_width: float = Field(ge=0.0)
    petal_length: float = Field(ge=0.0)
    petal_width: float = Field(ge=0.0)


class InferenceOut(Inference):
    """One instance of prediction for one class."""

    predicted_class: int
    probability: float = Field(ge=0.0)


class Predictor:

    def __init__(self, model_path: str):
        self.model_path = model_path
        self.session = self._load_model()

    def _load_model(self) -> rt.InferenceSession:
        """Helper function that  check if the given path is a valid one and laod the ONNX model.

        Raises:
            ValueError: the path is not valid

        Returns:
            rt.InferenceSession: An ONNX session
        """

        if Path(self.model_path).is_file() and Path(self.model_path).suffix == ".onnx":
            return rt.InferenceSession(
                self.model_path, providers=["CPUExecutionProvider"]
            )
        else:
            raise ValueError(
                f"{self.model_path} is not a valid path or a valid ONNX model"
            )

    def predict(self, features: InferenceIn) -> list[InferenceOut]:
        """Perform prediction.

        Args:
            features (InferenceIn): The features you want to predict.

        Returns:
            list[InferenceOut]: The list of predictions for all the classes of the dataset.
        """
        input_name = self.session.get_inputs()[0].name
        prob_name = self.session.get_outputs()[1].name

        # This part depends on the dataset you used.
        iris = np.array(
            [
                features.sepal_length,
                features.sepal_width,
                features.petal_length,
                features.petal_width,
            ]
        ).reshape(-1, 4)

        pred_onx = self.session.run([prob_name], {input_name: iris.astype(np.float32)})

        # We do not do batch predictions here, just prediction for one observation.
        classes = pred_onx[0][0]

        return [
            InferenceOut(predicted_class=k, probability=v) for k, v in classes.items()
        ]


model = Predictor(model_path="../models/svc_iris.onnx")


@router.post(
    "/inferences/",
    tags=["onnx"],
    response_model=list[InferenceOut],
    status_code=status.HTTP_200_OK,
    summary="Simple predictions with an ONNX model.",
)
def chat(features: InferenceIn):

    return model.predict(features=features)
