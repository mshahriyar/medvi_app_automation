"""
Validation configuration for all pages in the MEDVi automation project.
This file defines expected texts and images for each page to enable comprehensive validation.
"""

# Validation configurations for each page
PAGE_VALIDATION_CONFIGS = {
    'height_weight': {
        'texts': [
            'Reach your goal weight fast',
            'What is your height and weight?',
            'Feet',
            'Inches',
            'Weight (in lbs)',
            'Next'
        ],
        'images_by_src': [
            'wr_Romantic_lifestyle_photography_style_warm',
            'medvi-logo-soil.png',
            'treviews.png'
        ],
        'images_by_alt': [
            'MEDVi Logo',
            'TReviews Logo'
        ]
    },

    'goal_weight': {
        'texts': [
            'What is your goal weight?',
            'Next'
        ],
        'images_by_src': [
            # Main page images (if any)
        ],
        'images_by_alt': [
            # Main page images (if any)
        ],
        'header_texts': [
            # Header texts validated individually
        ],
        'header_images_by_src': [
            'treviews.png'
        ]
    },

    'gender_age': {
        'texts': [
            'Are you male or female?',
            'What is your age range?',
            'Next'
        ],
        'images_by_src': [
            # Main page images (if any)
        ],
        'images_by_alt': [
            # Main page images (if any)
        ],
        'header_texts': [
            # Header texts validated separately on main page
        ],
        'header_images_by_src': [
            'treviews.png'
        ]
    },

    'experience_illness': {
        'texts': [
            'Men over 40 experience',
            'unique effects',
            'from weight gain',
            'Do you experience any of the following?',
            'Low Libido',
            'Hair Loss',
            'Skin Issues',
            'Cognition',
            'None of these',
            'Next'
        ],
        'images_by_src': [
            # Main page images (if any)
        ],
        'images_by_alt': [
            # Main page images (if any)
        ],
        'header_texts': [
            # Header texts validated separately
        ],
        'header_images_by_src': [
            'treviews.png'
        ],
        'svg_icons': [
            'trending-down.svg',
            'medical',
            'health',
            'illness'
        ]
    },

    'priority': {
        'texts': [
            'Priority',
            'Goal',
            'Lose Weight',
            'Gain Muscle',
            'Maintain',
            'Next'
        ],
        'images_by_src': [
            'fitness',
            'goal',
            'priority'
        ]
    },

    'rank': {
        'texts': [
            'Forbes',
            'Number 1',
            'Ranking',
            'Congratulations',
            'Next'
        ],
        'images_by_src': [
            'forbes-number-1.png',
            'forbes',
            'ranking'
        ],
        'images_by_alt': [
            'Forbes Logo',
            'Number 1 Ranking'
        ]
    }
}

# Common elements that should be present on all pages
COMMON_ELEMENTS = {
    'texts': [
        'Next',
        'Continue',
        'Submit'
    ],
    'images_by_src': [
        'logo',
        'icon'
    ]
}

def get_validation_config(page_name: str) -> dict:
    """
    Get validation configuration for a specific page.

    Args:
        page_name: Name of the page (e.g., 'height_weight', 'rank')

    Returns:
        dict: Validation configuration for the page
    """
    config = PAGE_VALIDATION_CONFIGS.get(page_name, {})

    # Add common elements to the configuration
    if 'texts' not in config:
        config['texts'] = []
    if 'images_by_src' not in config:
        config['images_by_src'] = []
    if 'images_by_alt' not in config:
        config['images_by_alt'] = []
    if 'svg_icons' not in config:
        config['svg_icons'] = []

    # Merge with common elements
    config['texts'].extend(COMMON_ELEMENTS['texts'])
    config['images_by_src'].extend(COMMON_ELEMENTS['images_by_src'])

    return config

def get_all_page_names() -> list:
    """Get list of all available page names."""
    return list(PAGE_VALIDATION_CONFIGS.keys())

def get_validation_summary() -> dict:
    """
    Get a summary of validation configurations.

    Returns:
        dict: Summary with page names and element counts
    """
    summary = {}
    for page_name, config in PAGE_VALIDATION_CONFIGS.items():
        summary[page_name] = {
            'texts_count': len(config.get('texts', [])),
            'images_by_src_count': len(config.get('images_by_src', [])),
            'images_by_alt_count': len(config.get('images_by_alt', [])),
            'svg_icons_count': len(config.get('svg_icons', []))
        }
    return summary
