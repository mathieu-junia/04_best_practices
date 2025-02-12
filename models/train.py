from skl2onnx import __max_supported_opset__, convert_sklearn
from skl2onnx.common.data_types import FloatTensorType
from sklearn import datasets
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC

X, y = datasets.load_iris(return_X_y=True)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=1, stratify=y
)
svc_linear = SVC(kernel="linear", probability=True)
svc_linear.fit(X_train, y_train)

y_pred = svc_linear.predict(X_test)
accuracy_value = accuracy_score(y_test, y_pred)
print("accuracy:", accuracy_value)

initial_types = [
    ("float_input", FloatTensorType([None, svc_linear.n_features_in_])),
]

model_onnx = convert_sklearn(
    svc_linear,
    initial_types=initial_types,
    target_opset=__max_supported_opset__,
)

with open("svc_iris.onnx", "wb") as f:
    f.write(model_onnx.SerializeToString())
