from pgmpy.models import DiscreteBayesianNetwork
from pgmpy.factors.discrete import TabularCPD
from pgmpy.inference import VariableElimination

def create_student_performance_model():    
    model = DiscreteBayesianNetwork([
        ("Intelligence", "Grade"),
        ("StudyHours", "Grade"),
        ("Difficulty", "Grade"),
        ("Grade", "Pass")
    ])
    
    intel_cpd = TabularCPD(
        variable="Intelligence",
        variable_card=2,
        values=[[0.7], [0.3]],
        state_names={"Intelligence": ["High", "Low"]}
    )
    
    study_cpd = TabularCPD(
        variable="StudyHours",
        variable_card=2,
        values=[[0.6], [0.4]],
        state_names={"StudyHours": ["Sufficient", "Insufficient"]}
    )
    
    diff_cpd = TabularCPD(
        variable="Difficulty",
        variable_card=2,
        values=[[0.4], [0.6]],
        state_names={"Difficulty": ["Hard", "Easy"]}
    )
    
    grade_cpd = TabularCPD(
        variable="Grade",
        variable_card=3,
        values=[
            [0.7, 0.5, 0.5, 0.3, 0.4, 0.2, 0.2, 0.1],  # A
            [0.2, 0.3, 0.3, 0.4, 0.4, 0.4, 0.3, 0.3],  # B
            [0.1, 0.2, 0.2, 0.3, 0.2, 0.4, 0.5, 0.6]   # C
        ],
        evidence=["Intelligence", "StudyHours", "Difficulty"],
        evidence_card=[2, 2, 2],
        state_names={
            'Grade': ['A', 'B', 'C'],
            'Intelligence': ['High', 'Low'],
            'StudyHours': ['Sufficient', 'Insufficient'],
            'Difficulty': ['Hard', 'Easy']
        }
    )
    
    pass_cpd = TabularCPD(
        variable="Pass",
        variable_card=2,
        values=[[0.95, 0.80, 0.50], [0.05, 0.20, 0.50]],
        evidence=["Grade"],
        evidence_card=[3],
        state_names={
            "Pass": ["Yes", "No"],
            'Grade': ['A', 'B', 'C']
        }
    )
    
    model.add_cpds(intel_cpd, study_cpd, diff_cpd, grade_cpd, pass_cpd)
    
    if not model.check_model():
        raise ValueError("Model configuration is invalid")
    
    return model

def run_queries(model):
    infer_engine = VariableElimination(model)
    
    query1 = infer_engine.query(
        variables=['Pass'],
        evidence={'StudyHours': 'Sufficient', 'Difficulty': 'Hard'}
    )
    print("\nProbability of Passing (Given Sufficient Study and Hard Difficulty):")
    print(query1)
    
    query2 = infer_engine.query(
        variables=['Intelligence'],
        evidence={'Pass': 'Yes'}
    )
    print("\nProbability of High Intelligence (Given Passing):")
    print(query2)

def main():
    try:
        student_model = create_student_performance_model()
        run_queries(student_model)
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()