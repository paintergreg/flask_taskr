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

import os
from project import app
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="127.0.0.1", port=port)
