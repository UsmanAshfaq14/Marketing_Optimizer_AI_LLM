import json
import csv
from typing import Dict, List, Union
from dataclasses import dataclass
from io import StringIO

@dataclass
class CampaignData:
    channel: str
    sales_conversion: float
    click_through_rate: float
    customer_retention: float
    ad_spend: float

class MarketingOptimizer:
    def __init__(self):
        self.required_fields = [
            "channel", "sales_conversion", "click_through_rate",
            "customer_retention", "ad_spend"
        ]
        
    def validate_numeric_range(self, value: float, field: str) -> bool:
        if field in ["sales_conversion", "click_through_rate", "customer_retention"]:
            return 0 <= value <= 1
        elif field == "ad_spend":
            return value > 0
        return True

    def validate_data(self, campaigns: List[Dict]) -> tuple[bool, str]:
        if not campaigns:
            return False, "ERROR: No campaign data provided."
            
        for campaign in campaigns:
            # Check for missing fields
            missing_fields = [field for field in self.required_fields if field not in campaign]
            if missing_fields:
                return False, f"ERROR: Missing required field(s): {', '.join(missing_fields)}"
            
            # Validate data types and ranges
            for field in self.required_fields[1:]:  # Skip channel as it's a string
                try:
                    value = float(campaign[field])
                    if not self.validate_numeric_range(value, field):
                        return False, f"ERROR: Invalid value for field: {field}. Please check the allowed ranges."
                except ValueError:
                    return False, f"ERROR: Invalid data type for field: {field}. Please ensure numeric values."
                
        return True, "Data validation successful!"

    def calculate_performance_score(self, campaign: Dict) -> float:
        return (
            float(campaign["sales_conversion"]) * 0.4 +
            float(campaign["click_through_rate"]) * 0.3 +
            float(campaign["customer_retention"]) * 0.3
        )

    def determine_performance_category(self, score: float) -> str:
        if score >= 0.50:
            return "High Performance"
        elif score < 0.30:
            return "Low Performance"
        return "Moderate Performance"

    def get_budget_recommendation(self, category: str, ad_spend: float) -> str:
        if category == "High Performance":
            if ad_spend <= 10000:
                return "Increase investment for this channel."
            return "Maintain current investment; channel is performing well with significant spending."
        elif category == "Low Performance":
            if ad_spend > 15000:
                return "Decrease investment for this channel."
            return "Monitor performance; consider reducing investment if performance does not improve."
        return "Maintain or slightly adjust the current investment based on further review."

    def generate_report(self, data: str, format_type: str = "json") -> str:
        # Parse input data
        try:
            if format_type.lower() == "json":
                campaigns = json.loads(data)["campaigns"]
            else:  # CSV
                csv_data = StringIO(data)
                reader = csv.DictReader(csv_data)
                campaigns = list(reader)
        except Exception as e:
            return f"ERROR: Invalid data format. {str(e)}"

        # Validate data
        is_valid, message = self.validate_data(campaigns)
        if not is_valid:
            return message

        # Generate report
        report = [
            "# Data Validation Report",
            "## 1. Data Structure Check:",
            f"- Number of campaigns: {len(campaigns)}",
            f"- Number of fields per record: {len(self.required_fields)}",
            "",
            "## 2. Required Fields Check:",
            *[f"- {field}: ✓" for field in self.required_fields],
            "",
            "## 3. Data Type and Value Validation:",
            "- Sales Conversion (numeric between 0 and 1): ✓",
            "- Click Through Rate (numeric between 0 and 1): ✓",
            "- Customer Retention (numeric between 0 and 1): ✓",
            "- Ad Spend (positive number in USD): ✓",
            "",
            "## Validation Summary:",
            "Data validation is successful! Proceeding with analysis...",
            "",
            "# Formulas Used:",
            "1. **Performance Score Formula:**",
            "$\\text{Performance Score} = (\\text{sales\\_conversion} \\times 0.4) + (\\text{click\\_through\\_rate} \\times 0.3) + (\\text{customer\\_retention} \\times 0.3)$",
            "",
            "# Campaign Analysis Summary",
            f"Total Campaigns Evaluated: {len(campaigns)}",
            "",
            "# Detailed Analysis per Campaign",
        ]

        for campaign in campaigns:
            performance_score = self.calculate_performance_score(campaign)
            category = self.determine_performance_category(performance_score)
            recommendation = self.get_budget_recommendation(category, float(campaign["ad_spend"]))

            campaign_report = [
                f"## Campaign: {campaign['channel']}",
                "### Input Data:",
                f"- Sales Conversion: {float(campaign['sales_conversion']):.2f}",
                f"- Click Through Rate: {float(campaign['click_through_rate']):.2f}",
                f"- Customer Retention: {float(campaign['customer_retention']):.2f}",
                f"- Ad Spend: ${float(campaign['ad_spend']):,.2f}",
                "",
                "### Detailed Calculations:",
                "1. **Performance Score Calculation:**",
                f"   - Compute $\\text{{sales\\_conversion}} \\times 0.4$: ${float(campaign['sales_conversion']) * 0.4:.3f}$",
                f"   - Compute $\\text{{click\\_through\\_rate}} \\times 0.3$: ${float(campaign['click_through_rate']) * 0.3:.3f}$",
                f"   - Compute $\\text{{customer\\_retention}} \\times 0.3$: ${float(campaign['customer_retention']) * 0.3:.3f}$",
                f"   - Sum: ${float(campaign['sales_conversion']) * 0.4:.3f} + {float(campaign['click_through_rate']) * 0.3:.3f} + {float(campaign['customer_retention']) * 0.3:.3f} = {performance_score:.3f}$",
                f"   - Rounded Performance Score: {performance_score:.2f}",
                "",
                "2. **Performance Categorization:**",
                "   - If Performance Score $\\geq 0.50$: High Performance",
                "   - Else if Performance Score $< 0.30$: Low Performance",
                "   - Else: Moderate Performance",
                "",
                "### Final Recommendation:",
                f"- **Category:** {category}",
                f"- **Recommendation:** {recommendation}",
                ""
            ]
            report.extend(campaign_report)

        report.extend([
            "# Feedback and Rating",
            "Would you like detailed calculations for any specific campaign?",
            "Please rate this analysis on a scale of 1 to 5."
        ])

        return "\n".join(report)

if __name__ == "__main__":
    optimizer = MarketingOptimizer()

# Example JSON data
json_data = '''
                {
        "campaigns": [
            {
            "channel": "ChannelAlpha",
            "sales_conversion": 0.55,
            "click_through_rate": 0.40,
            "customer_retention": 0.50,
            "ad_spend": 7000
            },
            {
            "channel": "ChannelBeta",
            "sales_conversion": 0.65,
            "click_through_rate": 0.55,
            "customer_retention": 0.60,
            "ad_spend": 9000
            },
            {
            "channel": "ChannelGamma",
            "sales_conversion": 0.75,
            "click_through_rate": 0.65,
            "customer_retention": 0.70,
            "ad_spend": 11000
            },
            {
            "channel": "ChannelDelta",
            "sales_conversion": 0.45,
            "click_through_rate": 0.35,
            "customer_retention": 0.30,
            "ad_spend": 5000
            },
            {
            "channel": "ChannelEpsilon",
            "sales_conversion": 0.80,
            "click_through_rate": 0.75,
            "customer_retention": 0.85,
            "ad_spend": 15000
            },
            {
            "channel": "ChannelZeta",
            "sales_conversion": 0.60,
            "click_through_rate": 0.50,
            "customer_retention": 0.55,
            "ad_spend": 8000
            },
            {
            "channel": "ChannelEta",
            "sales_conversion": 0.50,
            "click_through_rate": 0.45,
            "customer_retention": 0.40,
            "ad_spend": 6000
            },
            {
            "channel": "ChannelTheta",
            "sales_conversion": 0.70,
            "click_through_rate": 0.60,
            "customer_retention": 0.65,
            "ad_spend": 13000
            },
            {
            "channel": "ChannelIota",
            "sales_conversion": 0.40,
            "click_through_rate": 0.30,
            "customer_retention": 0.35,
            "ad_spend": 4000
            },
            {
            "channel": "ChannelKappa",
            "sales_conversion": 0.85,
            "click_through_rate": 0.80,
            "customer_retention": 0.90,
            "ad_spend": 18000
            }
        ]
        }

    '''

report = optimizer.generate_report(json_data, "json")
print(report)