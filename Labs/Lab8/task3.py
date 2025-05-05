from pgmpy.models import DiscreteBayesianNetwork
from pgmpy.factors.discrete import TabularCPD
from pgmpy.inference import VariableElimination

def create_diagnosis_model():
    diagnosis_model = DiscreteBayesianNetwork([
        ("Disease", "Fever"),
        ("Disease", "Cough"), 
        ("Disease", "Fatigue"),
        ("Disease", "Chills")
    ])

    disease_cpd = TabularCPD(
        variable="Disease",
        variable_card=2,
        values=[[0.3], [0.7]],
        state_names={"Disease": ["Flu", "Cold"]}
    )

    fever_cpd = TabularCPD(
        variable="Fever",
        variable_card=2,
        values=[[0.9, 0.5], [0.1, 0.5]],
        evidence=["Disease"],
        evidence_card=[2],
        state_names={
            "Fever": ["Present", "Absent"],
            "Disease": ["Flu", "Cold"]
        }
    )

    cough_cpd = TabularCPD(
        variable="Cough",
        variable_card=2,
        values=[[0.8, 0.6], [0.2, 0.4]],
        evidence=["Disease"],
        evidence_card=[2],
        state_names={
            "Cough": ["Present", "Absent"],
            "Disease": ["Flu", "Cold"]
        }
    )

    fatigue_cpd = TabularCPD(
        variable="Fatigue",
        variable_card=2,
        values=[[0.7, 0.3], [0.3, 0.7]],
        evidence=["Disease"],
        evidence_card=[2],
        state_names={
            "Fatigue": ["Present", "Absent"],
            "Disease": ["Flu", "Cold"]
        }
    )

    chills_cpd = TabularCPD(
        variable="Chills",
        variable_card=2,
        values=[[0.6, 0.4], [0.4, 0.6]],
        evidence=["Disease"],
        evidence_card=[2],
        state_names={
            "Chills": ["Present", "Absent"],
            "Disease": ["Flu", "Cold"]
        }
    )

    diagnosis_model.add_cpds(
        disease_cpd, fever_cpd, cough_cpd, 
        fatigue_cpd, chills_cpd
    )

    if not diagnosis_model.check_model():
        raise ValueError("Model configuration is invalid")

    return diagnosis_model

def run_diagnostic_queries(model):
    diagnostic_engine = VariableElimination(model)

    result1 = diagnostic_engine.query(
        variables=["Disease"],
        evidence={"Fever": "Present", "Cough": "Present"}
    )
    print("\nDiagnosis given Fever and Cough:")
    print(result1)

    result2 = diagnostic_engine.query(
        variables=["Disease"],
        evidence={
            "Fever": "Present", 
            "Cough": "Present",
            "Chills": "Present"
        }
    )
    print("\nDiagnosis given Fever, Cough and Chills:")
    print(result2)

    result3 = diagnostic_engine.query(
        variables=["Fatigue"],
        evidence={"Disease": "Flu"}
    )
    print("\nFatigue probability given Flu:")
    print(result3)

def main():
    try:
        print("Medical Diagnosis Bayesian Network Analysis")
        print("----------------------------------------")
        
        diagnosis_model = create_diagnosis_model()
        run_diagnostic_queries(diagnosis_model)
        
    except Exception as e:
        print(f"An error occurred during diagnosis: {str(e)}")

if __name__ == "__main__":
    main()