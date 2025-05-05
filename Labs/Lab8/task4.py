import numpy as np

class WeatherSimulator:    
    def __init__(self):
        self.weather_states = ["Sunny", "Cloudy", "Rainy"]
        self.transition_matrix = [
            [0.33, 0.33, 0.34],
            [0.34, 0.33, 0.33],
            [0.33, 0.34, 0.33] 
        ]
        
    def validate_transition_matrix(self):
        for i, row in enumerate(self.transition_matrix):
            if not np.isclose(sum(row), 1.0):
                raise ValueError(f"Transition probabilities for {self.weather_states[i]} don't sum to 1")

    def simulate_weather(self, initial_state, days_to_simulate):
        self.validate_transition_matrix()
        
        if initial_state not in self.weather_states:
            raise ValueError("Invalid initial weather state")
            
        current_state = initial_state
        weather_sequence = [current_state]
        rainy_days = 0
        
        for _ in range(days_to_simulate):
            state_index = self.weather_states.index(current_state)
            transition_probs = self.transition_matrix[state_index]
            
            next_state = np.random.choice(
                self.weather_states,
                p=transition_probs
            )
            
            if next_state == "Rainy":
                rainy_days += 1
                
            weather_sequence.append(next_state)
            current_state = next_state
            
        return weather_sequence, rainy_days

def main():
    try:
        print("Weather Pattern Simulation")
        print("-------------------------")
        
        simulator = WeatherSimulator()
        initial_weather = "Sunny"
        simulation_days = 10
        
        weather_sequence, rainy_count = simulator.simulate_weather(
            initial_state=initial_weather,
            days_to_simulate=simulation_days
        )
        
        print(f"\n{simulation_days}-Day Weather Forecast:")
        print(" -> ".join(weather_sequence))
        
        rainy_probability = rainy_count / simulation_days
        print(f"\nProbability of rainy days: {rainy_probability:.2f} ({rainy_count}/{simulation_days} days)")
        
    except Exception as e:
        print(f"\nError during simulation: {str(e)}")

if __name__ == "__main__":
    main()