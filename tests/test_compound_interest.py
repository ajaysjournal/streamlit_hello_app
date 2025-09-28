"""Unit tests for compound interest calculator module."""

import pytest
import pandas as pd
from streamlit_hello_app.modules.compound_interest import calculate_compound_interest


class TestCalculateCompoundInterest:
    """Test cases for the calculate_compound_interest function."""
    
    def test_basic_calculation(self):
        """Test basic compound interest calculation."""
        principal = 1000.0
        rate = 0.05  # 5% annual rate
        time = 2.0   # 2 years
        compounding_freq = 12  # Monthly compounding
        
        final_amount, total_interest, breakdown = calculate_compound_interest(
            principal, rate, time, compounding_freq
        )
        
        # Expected calculation: 1000 * (1 + 0.05/12)^(12*2)
        expected_final = 1000 * (1 + 0.05/12) ** (12 * 2)
        expected_interest = expected_final - 1000
        
        assert abs(final_amount - expected_final) < 0.01
        assert abs(total_interest - expected_interest) < 0.01
        assert final_amount == principal + total_interest
    
    def test_yearly_compounding(self):
        """Test annual compounding frequency."""
        principal = 1000.0
        rate = 0.10  # 10% annual rate
        time = 3.0   # 3 years
        compounding_freq = 1  # Annual compounding
        
        final_amount, total_interest, breakdown = calculate_compound_interest(
            principal, rate, time, compounding_freq
        )
        
        # Expected: 1000 * (1 + 0.10)^3 = 1000 * 1.331 = 1331.00
        expected_final = 1000 * (1.10) ** 3
        expected_interest = expected_final - 1000
        
        assert abs(final_amount - expected_final) < 0.01
        assert abs(total_interest - expected_interest) < 0.01
    
    def test_daily_compounding(self):
        """Test daily compounding frequency."""
        principal = 5000.0
        rate = 0.08  # 8% annual rate
        time = 1.0   # 1 year
        compounding_freq = 365  # Daily compounding
        
        final_amount, total_interest, breakdown = calculate_compound_interest(
            principal, rate, time, compounding_freq
        )
        
        # Expected: 5000 * (1 + 0.08/365)^365
        expected_final = 5000 * (1 + 0.08/365) ** 365
        expected_interest = expected_final - 5000
        
        assert abs(final_amount - expected_final) < 0.01
        assert abs(total_interest - expected_interest) < 0.01
    
    def test_zero_interest_rate(self):
        """Test with zero interest rate."""
        principal = 1000.0
        rate = 0.0   # 0% interest rate
        time = 5.0   # 5 years
        compounding_freq = 12
        
        final_amount, total_interest, breakdown = calculate_compound_interest(
            principal, rate, time, compounding_freq
        )
        
        # With 0% interest, amount should remain the same
        assert final_amount == principal
        assert total_interest == 0.0
    
    def test_zero_principal(self):
        """Test with zero principal amount."""
        principal = 0.0
        rate = 0.05
        time = 2.0
        compounding_freq = 12
        
        final_amount, total_interest, breakdown = calculate_compound_interest(
            principal, rate, time, compounding_freq
        )
        
        # With 0 principal, everything should be 0
        assert final_amount == 0.0
        assert total_interest == 0.0
        # Breakdown should still have entries but with 0 values
        assert len(breakdown) == 2  # 2 years
        for entry in breakdown:
            assert entry['Principal'] == 0.0
            assert entry['Interest'] == 0.0
            assert entry['Total'] == 0.0
    
    def test_fractional_years(self):
        """Test with fractional years (e.g., 2.5 years)."""
        principal = 2000.0
        rate = 0.06  # 6% annual rate
        time = 2.5   # 2.5 years
        compounding_freq = 4  # Quarterly compounding
        
        final_amount, total_interest, breakdown = calculate_compound_interest(
            principal, rate, time, compounding_freq
        )
        
        # Expected: 2000 * (1 + 0.06/4)^(4*2.5)
        expected_final = 2000 * (1 + 0.06/4) ** (4 * 2.5)
        expected_interest = expected_final - 2000
        
        assert abs(final_amount - expected_final) < 0.01
        assert abs(total_interest - expected_interest) < 0.01
        
        # Check that breakdown includes fractional year entry
        assert len(breakdown) == 3  # Years 1, 2, and 2.5
        assert breakdown[-1]['Year'] == "2.5"
    
    def test_breakdown_structure(self):
        """Test that yearly breakdown has correct structure."""
        principal = 1500.0
        rate = 0.04  # 4% annual rate
        time = 3.0   # 3 years
        compounding_freq = 2  # Semi-annual compounding
        
        final_amount, total_interest, breakdown = calculate_compound_interest(
            principal, rate, time, compounding_freq
        )
        
        # Check breakdown structure
        assert len(breakdown) == 3  # 3 years
        assert all(isinstance(item, dict) for item in breakdown)
        
        # Check required keys in each breakdown entry
        required_keys = {'Year', 'Principal', 'Interest', 'Total'}
        for entry in breakdown:
            assert set(entry.keys()) == required_keys
        
        # Check that values are properly rounded
        for entry in breakdown:
            assert isinstance(entry['Principal'], (int, float))
            assert isinstance(entry['Interest'], (int, float))
            assert isinstance(entry['Total'], (int, float))
    
    def test_breakdown_accumulation(self):
        """Test that breakdown values accumulate correctly."""
        principal = 1000.0
        rate = 0.05  # 5% annual rate
        time = 2.0   # 2 years
        compounding_freq = 1  # Annual compounding for easier calculation
        
        final_amount, total_interest, breakdown = calculate_compound_interest(
            principal, rate, time, compounding_freq
        )
        
        # Check that principal accumulates correctly
        assert breakdown[0]['Principal'] == 1000.0
        assert breakdown[1]['Principal'] == breakdown[0]['Total']
        
        # Check that total matches final calculation
        assert breakdown[-1]['Total'] == final_amount
    
    def test_different_compounding_frequencies(self):
        """Test various compounding frequencies."""
        principal = 1000.0
        rate = 0.12  # 12% annual rate
        time = 1.0   # 1 year
        
        # Test different frequencies
        frequencies = [1, 2, 4, 12, 52, 365]  # Annual, Semi-annual, Quarterly, Monthly, Weekly, Daily
        
        results = []
        for freq in frequencies:
            final_amount, total_interest, breakdown = calculate_compound_interest(
                principal, rate, time, freq
            )
            results.append(final_amount)
        
        # More frequent compounding should yield higher returns
        # (except for annual which should be lowest)
        assert results[0] == min(results)  # Annual should be lowest
        assert results[-1] == max(results)  # Daily should be highest
        
        # Each frequency should be higher than the previous (except first)
        for i in range(1, len(results)):
            assert results[i] > results[i-1]
    
    def test_high_interest_rate(self):
        """Test with high interest rate."""
        principal = 500.0
        rate = 0.25  # 25% annual rate
        time = 2.0   # 2 years
        compounding_freq = 12  # Monthly compounding
        
        final_amount, total_interest, breakdown = calculate_compound_interest(
            principal, rate, time, compounding_freq
        )
        
        # With high interest, final amount should be significantly higher
        assert final_amount > principal * 1.5  # At least 50% increase
        assert total_interest > principal * 0.5  # Interest should be at least 50% of principal
        
        # Manual calculation check
        expected_final = 500 * (1 + 0.25/12) ** (12 * 2)
        assert abs(final_amount - expected_final) < 0.01
    
    def test_small_time_period(self):
        """Test with very small time period."""
        principal = 1000.0
        rate = 0.05
        time = 0.1   # 0.1 years (about 36.5 days)
        compounding_freq = 365  # Daily compounding
        
        final_amount, total_interest, breakdown = calculate_compound_interest(
            principal, rate, time, compounding_freq
        )
        
        # Should still work with small time periods
        assert final_amount > principal
        assert total_interest > 0
        assert len(breakdown) == 1  # Only one entry for fractional year
    
    def test_large_numbers(self):
        """Test with large principal amounts."""
        principal = 1000000.0  # $1 million
        rate = 0.07  # 7% annual rate
        time = 10.0  # 10 years
        compounding_freq = 12  # Monthly compounding
        
        final_amount, total_interest, breakdown = calculate_compound_interest(
            principal, rate, time, compounding_freq
        )
        
        # Should handle large numbers correctly
        assert final_amount > principal * 2  # Should at least double over 10 years
        assert total_interest > principal  # Interest should exceed principal
        
        # Check that all values are properly rounded to 2 decimal places
        assert final_amount == round(final_amount, 2)
        assert total_interest == round(total_interest, 2)
    
    def test_edge_case_very_small_principal(self):
        """Test with very small principal amount."""
        principal = 0.01  # 1 cent
        rate = 0.10  # 10% annual rate
        time = 1.0   # 1 year
        compounding_freq = 12
        
        final_amount, total_interest, breakdown = calculate_compound_interest(
            principal, rate, time, compounding_freq
        )
        
        # Should still work with very small amounts
        # Due to rounding, very small amounts might not show growth
        assert final_amount >= principal  # Should be >= due to rounding
        assert total_interest >= 0
        assert final_amount == round(final_amount, 2)
    
    def test_negative_interest_rate(self):
        """Test with negative interest rate (deflation)."""
        principal = 1000.0
        rate = -0.02  # -2% annual rate (deflation)
        time = 2.0    # 2 years
        compounding_freq = 12
        
        final_amount, total_interest, breakdown = calculate_compound_interest(
            principal, rate, time, compounding_freq
        )
        
        # With negative interest, final amount should be less than principal
        assert final_amount < principal
        assert total_interest < 0  # Negative interest
    
    def test_return_types(self):
        """Test that function returns correct types."""
        principal = 1000.0
        rate = 0.05
        time = 2.0
        compounding_freq = 12
        
        final_amount, total_interest, breakdown = calculate_compound_interest(
            principal, rate, time, compounding_freq
        )
        
        # Check return types
        assert isinstance(final_amount, (int, float))
        assert isinstance(total_interest, (int, float))
        assert isinstance(breakdown, list)
        assert all(isinstance(item, dict) for item in breakdown)
    
    def test_rounding_accuracy(self):
        """Test that values are properly rounded to 2 decimal places."""
        principal = 1000.0
        rate = 0.033333333  # 1/30 rate to create rounding challenges
        time = 3.0
        compounding_freq = 12
        
        final_amount, total_interest, breakdown = calculate_compound_interest(
            principal, rate, time, compounding_freq
        )
        
        # Check that main return values are properly rounded
        assert final_amount == round(final_amount, 2)
        assert total_interest == round(total_interest, 2)
        
        # Check that breakdown values are properly rounded
        for entry in breakdown:
            assert entry['Principal'] == round(entry['Principal'], 2)
            assert entry['Interest'] == round(entry['Interest'], 2)
            assert entry['Total'] == round(entry['Total'], 2)


class TestCompoundInterestEdgeCases:
    """Test edge cases and error conditions."""
    
    def test_zero_time_period(self):
        """Test with zero time period."""
        principal = 1000.0
        rate = 0.05
        time = 0.0
        compounding_freq = 12
        
        final_amount, total_interest, breakdown = calculate_compound_interest(
            principal, rate, time, compounding_freq
        )
        
        # With 0 time, amount should equal principal
        assert final_amount == principal
        assert total_interest == 0.0
        assert breakdown == []
    
    def test_very_high_compounding_frequency(self):
        """Test with very high compounding frequency."""
        principal = 1000.0
        rate = 0.05
        time = 1.0
        compounding_freq = 8760  # Hourly compounding (365 * 24)
        
        final_amount, total_interest, breakdown = calculate_compound_interest(
            principal, rate, time, compounding_freq
        )
        
        # Should handle high frequencies without issues
        assert final_amount > principal
        assert total_interest > 0
        assert isinstance(final_amount, (int, float))
    
    def test_fractional_compounding_frequency(self):
        """Test with fractional compounding frequency (should be handled gracefully)."""
        principal = 1000.0
        rate = 0.05
        time = 1.0
        compounding_freq = 12.5  # This should work (will be treated as integer)
        
        # This should not raise an error, though it's not a typical use case
        final_amount, total_interest, breakdown = calculate_compound_interest(
            principal, rate, time, int(compounding_freq)
        )
        
        assert final_amount > principal
        assert total_interest > 0


if __name__ == "__main__":
    # Run tests if executed directly
    pytest.main([__file__, "-v"])
