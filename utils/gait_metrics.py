import os
import pandas as pd
import numpy as np
import glob
from typing import List, Dict, Tuple

# Gold standard gait phase percentages from the paper
GOLD_STANDARD = {
    "Initial-LSw": 13.0,
    "Mid-LSw": 14.0,
    "Term-LSw": 13.0,
    "DSt1": 10.0,
    "Initial-RSw": 13.0,
    "Mid-RSw": 14.0,
    "Term-RSw": 13.0,
    "DSt2": 10.0
}

def find_gait_cycles(df: pd.DataFrame, reference_phase: str = "DSt1") -> List[List[int]]:
    """
    Find complete gait cycles in the DataFrame.
    A complete cycle starts at one occurrence of the reference_phase and
    ends right before the next occurrence of the reference_phase.
    
    Args:
        df: DataFrame containing gait phase data
        reference_phase: The reference phase that marks the start/end of a cycle
        
    Returns:
        List of lists containing indices for each complete cycle
    """
    # Find indices where the reference phase occurs
    reference_indices = df.index[df['gait_phase'] == reference_phase].tolist()
    
    if not reference_indices:
        return []
    
    # Create cycles from one reference phase to the next
    cycles = []
    for i in range(len(reference_indices) - 1):
        start_idx = reference_indices[i]
        end_idx = reference_indices[i+1]
        # Include all frames from start up to (but not including) end
        cycle = list(range(start_idx, end_idx))
        cycles.append(cycle)
    
    # Filter out incomplete cycles (should have all expected phase types)
    complete_cycles = []
    for cycle in cycles:
        cycle_phases = set(df.iloc[cycle]['gait_phase'])
        if cycle_phases.issuperset(GOLD_STANDARD.keys()):
            complete_cycles.append(cycle)
    
    return complete_cycles

def calculate_phase_percentages(df: pd.DataFrame, cycle_indices: List[int]) -> Dict[str, float]:
    """
    Calculate the percentage of each gait phase in a cycle.
    
    Args:
        df: DataFrame containing gait phase data
        cycle_indices: List of indices for one complete cycle
        
    Returns:
        Dictionary mapping phase names to their percentages in the order they occur
    """
    cycle_length = len(cycle_indices)
    phases = df.iloc[cycle_indices]['gait_phase']
    
    # Count occurrences of each phase
    phase_counts = {}
    for phase in GOLD_STANDARD.keys():
        count = sum(phases == phase)
        phase_counts[phase] = count
    
    # Calculate percentages
    percentages = {}
    for phase, count in phase_counts.items():
        percentages[phase] = (count / cycle_length) * 100
    
    return percentages

def calculate_errors(actual: Dict[str, float], gold: Dict[str, float]) -> Tuple[Dict[str, float], Dict[str, float]]:
    """
    Calculate absolute and relative errors between actual and gold standard percentages.
    
    Args:
        actual: Dictionary mapping phase names to their actual percentages
        gold: Dictionary mapping phase names to their gold standard percentages
        
    Returns:
        Tuple of (absolute_errors, relative_errors) dictionaries
    """
    absolute_errors = {}
    relative_errors = {}
    
    for phase in gold.keys():
        absolute_errors[phase] = abs(actual[phase] - gold[phase])
        relative_errors[phase] = (absolute_errors[phase] / gold[phase]) * 100 if gold[phase] > 0 else 0
    
    return absolute_errors, relative_errors

def validate_gait_cycles(base_path: str, max_cycles: int = None, reference_phase: str = "DSt1", modified=True) -> None:
    """
    Validate gait cycles against gold standard percentages and save results.
    
    Args:
        base_path: Base path to search for gait classification data
        max_cycles: Maximum number of cycles to analyze, None for all
        reference_phase: The reference phase that marks the start/end of a cycle
    """
    # Find the CSV file in the gait-classification directory
    if modified:
        gait_classification_dir = os.path.join(base_path, "gait-classification")
        csv_path = os.path.join(gait_classification_dir, "*_original.csv")
    else:
        gait_classification_dir = os.path.join(base_path, "gait-classification-paper")
        csv_path = os.path.join(gait_classification_dir, "*_paper_original.csv")
    csv_files = glob.glob(csv_path)
    
    if not csv_files:
        print(f"No _original.csv file found in {gait_classification_dir}")
        return
    
    # There should only be one _original.csv file
    csv_file = csv_files[0]
    print(f"Processing {csv_file}")
    
    # Read the CSV file
    df = pd.read_csv(csv_file)
    
    # Find complete gait cycles
    cycles = find_gait_cycles(df, reference_phase)
    print(f"Found {len(cycles)} complete cycles starting with {reference_phase}")
    
    # Limit the number of cycles if specified
    if max_cycles is not None and len(cycles) > max_cycles:
        print(f"Limiting analysis to {max_cycles} cycles")
        cycles = cycles[:max_cycles]
    
    all_results = []
    phase_results = {phase: {"absolute_errors": [], "relative_errors": []} for phase in GOLD_STANDARD.keys()}
    
    # Calculate metrics for each cycle
    for i, cycle_indices in enumerate(cycles):
        print(f"Analyzing cycle {i+1} (frames {cycle_indices[0]}-{cycle_indices[-1]})")
        
        # Calculate percentages for this cycle
        actual_percentages = calculate_phase_percentages(df, cycle_indices)
        absolute_errors, relative_errors = calculate_errors(actual_percentages, GOLD_STANDARD)
        
        # Get sequence of phases in this cycle
        cycle_phases = df.iloc[cycle_indices]['gait_phase'].tolist()
        # Get unique phases in cycle in order of first appearance
        phase_order = []
        for phase in cycle_phases:
            if phase not in phase_order:
                phase_order.append(phase)
        
        # Add results for this cycle
        for phase in phase_order:
            if phase in GOLD_STANDARD:
                # Store results for detailed metrics.csv
                result = {
                    "Cycle": i + 1,
                    "Phase": phase,
                    "Gold Standard": GOLD_STANDARD[phase],
                    "Actual Percentage": actual_percentages[phase],
                    "Absolute Error": absolute_errors[phase],
                    "Relative Error": relative_errors[phase]
                }
                all_results.append(result)
                
                # Store errors for summary calculation
                phase_results[phase]["absolute_errors"].append(absolute_errors[phase])
                phase_results[phase]["relative_errors"].append(relative_errors[phase])
    
    # Create and save detailed results DataFrame
    if all_results:
        # Save detailed metrics
        results_df = pd.DataFrame(all_results)
        output_path = os.path.join(gait_classification_dir, "metrics.csv")
        results_df.to_csv(output_path, index=False)
        print(f"Detailed results saved to {output_path}")
        
        # Create and save summary metrics (average across all cycles)
        summary_results = []
        for phase in GOLD_STANDARD.keys():
            abs_errors = phase_results[phase]["absolute_errors"]
            rel_errors = phase_results[phase]["relative_errors"]
            
            if abs_errors and rel_errors:  # Check if we have data for this phase
                summary_result = {
                    "Phase": phase,
                    "Gold Standard": GOLD_STANDARD[phase],
                    "Avg Actual Percentage": results_df[results_df["Phase"] == phase]["Actual Percentage"].mean(),
                    "Avg Absolute Error": sum(abs_errors) / len(abs_errors),
                    "Avg Relative Error": sum(rel_errors) / len(rel_errors)
                }
                summary_results.append(summary_result)
        
        if summary_results:
            summary_df = pd.DataFrame(summary_results)
            summary_path = os.path.join(gait_classification_dir, "metrics_summary.csv")
            summary_df.to_csv(summary_path, index=False)
            print(f"Summary metrics saved to {summary_path}")
    else:
        print("No complete gait cycles found")