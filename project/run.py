#! /usr/bin/env python3
#
################
#
# project/run.py
#
################
#

"""
    Script starts the Tasker application
"""

from views import app
if __name__ == "__main__":
    app.run(debug=True)
