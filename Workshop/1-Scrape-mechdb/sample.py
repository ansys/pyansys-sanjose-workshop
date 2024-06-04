'''
note - rename to pymechanical
'''
import os
import typing

import ansys.mechanical.core as mech
app=mech.App(version=241)
globals().update(mech.global_variables(app, True))
FILES_PATH = os.path.join(__file__, os.pardir, "Files")

class Problems:
    RIGID_REMOTE_POINT_ON_BEAM_CONNECTION = """
A beam connection uses a rigid connection!
"""

    RIGID_REMOTE_POINT_ON_BEARING = """
A bearing uses a rigid connection!
"""

    WEAK_SPRINGS_ENABLED = """
An analysis has weak springs enabled!
"""

def has_weak_springs():
    return False

def has_rigid_beam():
    return False

def has_rigid_bearing():
    return False

def get_problems(mechdb: str) -> typing.List[str]:
    app.open(os.path.join(FILES_PATH, mechdb))
    problems = []
    if (has_weak_springs()):
        problems.append(Problems.WEAK_SPRINGS_ENABLED)
    if (has_rigid_beam()):
        problems.append(Problems.RIGID_REMOTE_POINT_ON_BEAM_CONNECTION)
    if (has_rigid_bearing()):
        problems.append(Problems.RIGID_REMOTE_POINT_ON_BEARING)
    return problems

def report_problem(mechdb: str, problem: str):
    print(f"{mechdb} has a problem: {problem}")

def report_no_problem(mechdb: str):
    print(f"{mechdb} has no problems")

def test_mechdbs():
    mechdbs = [file for file in os.listdir(FILES_PATH) if file.endswith(".mechdb")]
    for mechdb in mechdbs:
        problems = get_problems(os.path.join(mechdb))
        if len(problems) == 0:
            report_no_problem(mechdb)
        for problem in problems:
            report_problem(mechdb, problem)

if __name__ == "__main__":
    try:
        test_mechdbs()
    finally:
        app.new()  # This ensures that there are no leftover lock files