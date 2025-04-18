import pytest
from unittest.mock import MagicMock
from ShinyTB import server

# Test when the button has not been clicked
def test_sim_plot_button_not_clicked():
    # Mock the input.simulate() method to return False
    input_mock = MagicMock()
    input_mock.simulate.return_value = False

    # Call the sim_plot method
    fig = sim_plot(input_mock)

    # Assert that the returned figure has no axes
    assert fig.axes == []

# Test when there is no simulation data available
def test_sim_plot_no_data():
    # Mock the simulation_result.get() method to return None
    simulation_result_mock = MagicMock()
    simulation_result_mock.get.return_value = None

    # Call the sim_plot method
    fig = sim_plot(simulation_result_mock)

    # Assert that the returned figure has a text with the correct message
    ax = fig.axes[0]
    assert ax.texts[0].get_text() == "No simulation data available."

# Test when there is simulation data available
def test_sim_plot_with_data():
    # Mock the simulation_result.get() method to return a valid result
    simulation_result_mock = MagicMock()
    result = {
        "fig": plt.figure()
    }
    simulation_result_mock.get.return_value = result

    # Call the sim_plot method
    fig = sim_plot(simulation_result_mock)

    # Assert that the returned figure is the same as the mocked result
    assert fig == result["fig"]
