# Workshop 1: Scrape mechdb files

# Problem statement
There is a problem at your organization, an important simulation model does not match experiments. After three weeks of intense investigation, a senior analyst has discovered the cause, and now makes the following recommendations:

- The `Weak Springs` option  under `Analysis Settings` has to be set to `No`, for applicable analyses
- Both `Beam Connections` and `Bearings` can not use a `Rigid` scoping, whether it is applied directly via Geometry Selection or indirectly using a remote point

The analyst has identified a set of projects that may be affected. There are thousands of them in the PLM system. They would like for you to check for these problems in all of these projects, and report back which of them have which problem.

# Workspace
See `sample.py` for an outline of a python program. In the `Files` folder, there are some sample projects that may contain the above problems. Modify `sample.py` so that it prints out which projects are affected by which problems. Once you have done this, you can use it on the thousands of projects in the PLM system.

# Expected result
AB_1.mechdb has the following problems:
    A beam connection uses a rigid connection!
AB_2.mechdb has no problems
AB_3.mechdb has the following problems:
    An analysis has weak springs enabled!
AB_5.mechdb has the following problems:
    A beam connection uses a rigid connection!
OO_1.mechdb has no problems
OO_2.mechdb has the following problems:
    A bearing uses a rigid connection!