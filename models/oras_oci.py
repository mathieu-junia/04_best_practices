import numpy as np
import onnxruntime as rt
import oras.client
import oras.oci
import oras.provider
from sklearn import datasets
from sklearn.model_selection import train_test_split

X, y = datasets.load_iris(return_X_y=True)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=1, stratify=y
)

client = oras.client.OrasClient(insecure=True)
client.push(files=["svc_iris.onnx"], target="localhost:5000/isen/svc_iris:v1")

model = client.pull(target="localhost:5000/isen/svc_iris:v1", outdir="model")
print(model)

sess = rt.InferenceSession(model[0], providers=["CPUExecutionProvider"])
input_name = sess.get_inputs()[0].name
print(input_name)
label_name = sess.get_outputs()[0].name
print(label_name)
prob_name = sess.get_outputs()[1].name
print(prob_name)
pred_onx = sess.run([label_name], {input_name: X_test.astype(np.float32)})
print("prediction:", pred_onx)
