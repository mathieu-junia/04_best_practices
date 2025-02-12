import numpy as np
import onnxruntime as rt
from sklearn import datasets
from sklearn.model_selection import train_test_split
from pydantic import BaseModel

X, y = datasets.load_iris(return_X_y=True)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=1, stratify=y
)

sess = rt.InferenceSession("svc_iris.onnx", providers=["CPUExecutionProvider"])
input_name = sess.get_inputs()[0].name
print(input_name)
label_name = sess.get_outputs()[0].name
print(label_name)
prob_name = sess.get_outputs()[1].name
print(prob_name)
pred_onx = sess.run([label_name], {input_name: X_test.astype(np.float32)})
print("prediction:", pred_onx)


class Iris(BaseModel):
  sepal_length: float
  sepal_width: float
  petal_length: float
  petal_width: float


iris_value = Iris(
  sepal_length=1,
  sepal_width=0.4,
  petal_length=0.685,
  petal_width=2,
)

iris = np.array([iris_value.sepal_length,iris_value.sepal_width,iris_value.petal_length,iris_value.petal_width]).reshape(-1,4)

pred_onx = sess.run([prob_name], {input_name: iris.astype(np.float32)})
print("prediction:", pred_onx)
