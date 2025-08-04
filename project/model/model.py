import pickle

with open('model/model.pkl', 'rb') as f:
    model = pickle.load(f)

MODEL_VERSION='1.0.0'


def model_prediction(input_df):

    classes=model.classes_.tolist()
    predicted_class= model.predict(input_df)[0] 
    probabilities=model.predict_proba(input_df)[0].tolist()
    confidence=max(probabilities)
    class_prob=dict(zip(classes,probabilities))

    return {
        'predicted_category':predicted_class,
        'confidence':confidence,
        'class_probabilities':class_prob
    }

