# --------------------------------------------
#   Version: 0.2.0
#   Creators: Elliott Chimienti, Zane Little
#   Support us!: https://ko-fi.com/flhourcounterguys
# -------------------------------------------

import FLP, struct, glob, os, fnmatch, sys, gc
import PySimpleGUI as sg
import webbrowser
from datetime import datetime,timedelta,date
import os.path
from FLP import FLPFile
from sys import argv

if sys.platform.startswith('win'):
    import ctypes
    if sys.argv[0].endswith('.exe') == False:
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(u'CompanyName.ProductName.SubProduct.VersionInformation') # Arbitrary string

g_hjob = None
def mprint(*args, **kwargs):
    window['-ML-'].print(*args, **kwargs)
print = mprint

# Program Window Icon
ico = b'iVBORw0KGgoAAAANSUhEUgAAAGQAAABkCAYAAABw4pVUAAABKGlDQ1BBZG9iZSBSR0IgKDE5OTgpAAAoz2NgYDJwdHFyZRJgYMjNKykKcndSiIiMUmA/z8DGwMwABonJxQWOAQE+IHZefl4qAypgZGD4dg1EMjBc1gWZxUAa4EouKCoB0n+A2CgltTgZaKQBkJ1dXlIAFGecA2SLJGWD2RtA7KKQIGcg+wiQzZcOYV8BsZMg7CcgdhHQE0D2F5D6dDCbiQNsDoQtA2KXpFaA7GVwzi+oLMpMzyhRMLS0tFRwTMlPSlUIriwuSc0tVvDMS84vKsgvSixJTQGqhbgPDAQhCkEhpgHUaKHJQGUAigcI63MgOHwZxc4gxBAgubSoDBYXTMaE+Qgz5kgwMPgvZWBg+YMQM+llYFigw8DAPxUhpmbIwCCgz8Cwbw4AwrNP/sZG7OUAAAAJcEhZcwAACxMAAAsTAQCanBgAAAqxaVRYdFhNTDpjb20uYWRvYmUueG1wAAAAAAA8P3hwYWNrZXQgYmVnaW49Iu+7vyIgaWQ9Ilc1TTBNcENlaGlIenJlU3pOVGN6a2M5ZCI/PiA8eDp4bXBtZXRhIHhtbG5zOng9ImFkb2JlOm5zOm1ldGEvIiB4OnhtcHRrPSJBZG9iZSBYTVAgQ29yZSA2LjAtYzAwMiA3OS4xNjQzNTIsIDIwMjAvMDEvMzAtMTU6NTA6MzggICAgICAgICI+IDxyZGY6UkRGIHhtbG5zOnJkZj0iaHR0cDovL3d3dy53My5vcmcvMTk5OS8wMi8yMi1yZGYtc3ludGF4LW5zIyI+IDxyZGY6RGVzY3JpcHRpb24gcmRmOmFib3V0PSIiIHhtbG5zOnhtcD0iaHR0cDovL25zLmFkb2JlLmNvbS94YXAvMS4wLyIgeG1sbnM6ZGM9Imh0dHA6Ly9wdXJsLm9yZy9kYy9lbGVtZW50cy8xLjEvIiB4bWxuczpwaG90b3Nob3A9Imh0dHA6Ly9ucy5hZG9iZS5jb20vcGhvdG9zaG9wLzEuMC8iIHhtbG5zOnhtcE1NPSJodHRwOi8vbnMuYWRvYmUuY29tL3hhcC8xLjAvbW0vIiB4bWxuczpzdEV2dD0iaHR0cDovL25zLmFkb2JlLmNvbS94YXAvMS4wL3NUeXBlL1Jlc291cmNlRXZlbnQjIiB4bWxuczpzdFJlZj0iaHR0cDovL25zLmFkb2JlLmNvbS94YXAvMS4wL3NUeXBlL1Jlc291cmNlUmVmIyIgeG1wOkNyZWF0b3JUb29sPSJBZG9iZSBQaG90b3Nob3AgMjEuMSAoV2luZG93cykiIHhtcDpDcmVhdGVEYXRlPSIyMDIxLTExLTE0VDE3OjUwOjExLTA4OjAwIiB4bXA6TW9kaWZ5RGF0ZT0iMjAyMS0xMS0xNFQxOTozOTozMC0wODowMCIgeG1wOk1ldGFkYXRhRGF0ZT0iMjAyMS0xMS0xNFQxOTozOTozMC0wODowMCIgZGM6Zm9ybWF0PSJpbWFnZS9wbmciIHBob3Rvc2hvcDpDb2xvck1vZGU9IjMiIHBob3Rvc2hvcDpJQ0NQcm9maWxlPSJBZG9iZSBSR0IgKDE5OTgpIiB4bXBNTTpJbnN0YW5jZUlEPSJ4bXAuaWlkOmU2ZWU0ZDQxLTE2ODctYTQ0NC05YTllLTg4MjYyZDQ3NTJhOCIgeG1wTU06RG9jdW1lbnRJRD0iYWRvYmU6ZG9jaWQ6cGhvdG9zaG9wOmFhZTFmNWU2LTMxOWMtN2U0Ny04Y2U0LWQwZmM1NTVlMGRjMyIgeG1wTU06T3JpZ2luYWxEb2N1bWVudElEPSJ4bXAuZGlkOjRlOTY4YjlhLTAwOTktYTY0OS05MWI2LThhYjkzYTkyZDMwZSI+IDx4bXBNTTpIaXN0b3J5PiA8cmRmOlNlcT4gPHJkZjpsaSBzdEV2dDphY3Rpb249ImNyZWF0ZWQiIHN0RXZ0Omluc3RhbmNlSUQ9InhtcC5paWQ6NGU5NjhiOWEtMDA5OS1hNjQ5LTkxYjYtOGFiOTNhOTJkMzBlIiBzdEV2dDp3aGVuPSIyMDIxLTExLTE0VDE3OjUwOjExLTA4OjAwIiBzdEV2dDpzb2Z0d2FyZUFnZW50PSJBZG9iZSBQaG90b3Nob3AgMjEuMSAoV2luZG93cykiLz4gPHJkZjpsaSBzdEV2dDphY3Rpb249ImNvbnZlcnRlZCIgc3RFdnQ6cGFyYW1ldGVycz0iZnJvbSBpbWFnZS9wbmcgdG8gYXBwbGljYXRpb24vdm5kLmFkb2JlLnBob3Rvc2hvcCIvPiA8cmRmOmxpIHN0RXZ0OmFjdGlvbj0ic2F2ZWQiIHN0RXZ0Omluc3RhbmNlSUQ9InhtcC5paWQ6ZWUxMTk0NmQtY2ZhZi02MTQ1LTlkZjItMjFlNzJiZDlhNTliIiBzdEV2dDp3aGVuPSIyMDIxLTExLTE0VDE5OjE4OjE4LTA4OjAwIiBzdEV2dDpzb2Z0d2FyZUFnZW50PSJBZG9iZSBQaG90b3Nob3AgMjEuMSAoV2luZG93cykiIHN0RXZ0OmNoYW5nZWQ9Ii8iLz4gPHJkZjpsaSBzdEV2dDphY3Rpb249InNhdmVkIiBzdEV2dDppbnN0YW5jZUlEPSJ4bXAuaWlkOjFlYzc2YzllLTBhOWQtNjQ0Zi1hODZkLWJkYzE1ZjU2ZDBjYSIgc3RFdnQ6d2hlbj0iMjAyMS0xMS0xNFQxOToyMzoxNy0wODowMCIgc3RFdnQ6c29mdHdhcmVBZ2VudD0iQWRvYmUgUGhvdG9zaG9wIDIxLjEgKFdpbmRvd3MpIiBzdEV2dDpjaGFuZ2VkPSIvIi8+IDxyZGY6bGkgc3RFdnQ6YWN0aW9uPSJjb252ZXJ0ZWQiIHN0RXZ0OnBhcmFtZXRlcnM9ImZyb20gYXBwbGljYXRpb24vdm5kLmFkb2JlLnBob3Rvc2hvcCB0byBpbWFnZS9wbmciLz4gPHJkZjpsaSBzdEV2dDphY3Rpb249ImRlcml2ZWQiIHN0RXZ0OnBhcmFtZXRlcnM9ImNvbnZlcnRlZCBmcm9tIGFwcGxpY2F0aW9uL3ZuZC5hZG9iZS5waG90b3Nob3AgdG8gaW1hZ2UvcG5nIi8+IDxyZGY6bGkgc3RFdnQ6YWN0aW9uPSJzYXZlZCIgc3RFdnQ6aW5zdGFuY2VJRD0ieG1wLmlpZDozYWFkYTVmNi05OWUzLWNiNGUtYjIzZi05Y2NjMjY3OGFjNGMiIHN0RXZ0OndoZW49IjIwMjEtMTEtMTRUMTk6MjM6MTctMDg6MDAiIHN0RXZ0OnNvZnR3YXJlQWdlbnQ9IkFkb2JlIFBob3Rvc2hvcCAyMS4xIChXaW5kb3dzKSIgc3RFdnQ6Y2hhbmdlZD0iLyIvPiA8cmRmOmxpIHN0RXZ0OmFjdGlvbj0ic2F2ZWQiIHN0RXZ0Omluc3RhbmNlSUQ9InhtcC5paWQ6ZTZlZTRkNDEtMTY4Ny1hNDQ0LTlhOWUtODgyNjJkNDc1MmE4IiBzdEV2dDp3aGVuPSIyMDIxLTExLTE0VDE5OjM5OjMwLTA4OjAwIiBzdEV2dDpzb2Z0d2FyZUFnZW50PSJBZG9iZSBQaG90b3Nob3AgMjEuMSAoV2luZG93cykiIHN0RXZ0OmNoYW5nZWQ9Ii8iLz4gPC9yZGY6U2VxPiA8L3htcE1NOkhpc3Rvcnk+IDx4bXBNTTpEZXJpdmVkRnJvbSBzdFJlZjppbnN0YW5jZUlEPSJ4bXAuaWlkOjFlYzc2YzllLTBhOWQtNjQ0Zi1hODZkLWJkYzE1ZjU2ZDBjYSIgc3RSZWY6ZG9jdW1lbnRJRD0ieG1wLmRpZDo0ZTk2OGI5YS0wMDk5LWE2NDktOTFiNi04YWI5M2E5MmQzMGUiIHN0UmVmOm9yaWdpbmFsRG9jdW1lbnRJRD0ieG1wLmRpZDo0ZTk2OGI5YS0wMDk5LWE2NDktOTFiNi04YWI5M2E5MmQzMGUiLz4gPC9yZGY6RGVzY3JpcHRpb24+IDwvcmRmOlJERj4gPC94OnhtcG1ldGE+IDw/eHBhY2tldCBlbmQ9InIiPz5ADt0SAAAa1ElEQVR42u2dCXRURdbH22VcEFHRUYEEdXRGWYeQBQJoWARC2OUbQTkzgg46nyK4DOAnIgzILmIMCYQlhAQIiwLKCINsosgqiIpIkD0QIEhWIKDo/epW9319X716r9do1Hnn/E83ISTd79f/e+tW1S1cAOAizVk7pbIJKlCV6r0SA1clBgI/kf4LpBLBqDRQfAJ58sknA9Ljjz/uysrKci1fvtw1YcIEV9u2bV2ZmZlSI0aMcPXp08fVpk0b1+uvv+56/vnnXS+88IKt+M264oorpC6//HJDl112mUUu8VYCkQrFxa74F2q4Wo2q5Wo5oqYr/vkaFaJKBeTFF190LViwwNWrVy+t6CalLZ0IV155pQVKOICoUP4LRADB53379nU99thjhvhNuuqqqyQQFH2t86OJUO3G6wMGcsWVV0Ddxveavtald3sOpSvCaD7o9t82kMGDB7v69evnSkhIkOJAfve730lxIOEQAbn+hqoWlyQMryWBsK+v/M0BeeKJJ1wrVqyQf1YdUpFArru+iunrrUZG2A4ofpNA1Jtw9dVXW4BMf/8NePjv3aB69epQ+67IkID0H/5EQP/uNwHE6QYgEHIJArjpppsM3XjjjXDDDTdYVK1aNYtuqn4TDHl9gAXIoPHP2P7uDumR0GFa5G8HiK9PY4+/dYFrrrlGAkHdfPPNBhSEQfIXChcBGT3zZcvvfSHzETcMCSTC9HdNB9ZwhUuVBogThMzVKVCzZk24/fbb4bbbboNbb70Vrr32WrjlllskDJIvl/iCQkD416QrpkcyGJG/7pAlfuZ6HYTkeWPhD3/4A9SuXRsiIiKgVq1aUKNGDRMUBIIOIZegqlSpEpJLVBkghAbO6qn9wIjvc4VLPysQ8fPy1Dd3f5vm8Kc//QnuueceCeTOO++EyMhIKXIJCoH8/ve/lxDwU/3JJ5/Axo0b4eOPP5b66KOPpDZs2CBFdcmHH34I27Ztg7vvvlsOCuxAXHd1NUhizqh6jfvrPfp0rlAoPxsQS1haMwUaNGgAdevWhfvuu8+Actddd8Edd9whgaBTEAY647PPPoOtW7fCli1bYPPmzVKbNm1yBIMwuPDrFKbwOYZBvOk317jBBEMHLGNVcoVA+cmB6D5dU94eD40aNYKGDRtC/fr1oU6dOnDvvffCH//4R8MlGLqGDBkCO3fuhB07dsCnn34K27dvl592DoagcDCqWwjI+vXrYd26dfKRnm/auBmSZkS6gcyI9BnSNO9n1C8GiA5GXFwcxMbGQuPGjeHPf/6zxSX4iI4Qw2H4/PPPYdeuXdIdBAah6MCgnMBwpxAQlIQhlJgeIQHl5OQEAwUqPRD1Bbdo0QKaNWsGTZs2hSZNmkBMTAxERUUZLjl48CDk5ubC119/DXv27IGvvvoKdu/eDV9++aUBZsP+d6Hrwgjotqg2dFvoVpf5NSFr91iLY9QwpnMLwUB3kHPwsX///pbRl6rRM4eGBcpPAkR9oQkJCXD//fdD8+bNIT4+XkLhLhkwYADs378fvvnmG9i3bx/s3bvXAJP+2cvw0Nu13VpcG7ozGN0WCM0XmlcbuqLmRlqg2Lll8RdTDSDcMQQFgeBz/Dl2UHAUFyqUCgeivsBWrVpJIRRyCUJBlxw9ehSOHDkChw8fhkOHDsGBAwcMMBv3rYSHltT2wvAA4e7olsOAzBVuyY50K0uA2eQGYweFYGzbuckCQ6dAQlilAaK+sAcffBBEEQitW7eGli1bGi5Bdxw/fhyOHTsGeXl5EgxCITBJi25xw3hHA2Qh03y3unIgAkaXOW69uq63xS0IJGfHm0aoUsOYE5yKgFJhQNQXJIa7UgSEXIKjq5MnT0rl5+dLERiE1GPpHdBjyR1mIIs14Wq+Eq7IHdluGJ1RsyOhTXp1y0iMYGzJXWfJLXw0xkXDZRwNhhNKhQBRX0i7du0MIRCCcubMGfj222/h9OnTUFBQAKdOnfKCOZ5vhrHE7AwJZKEfQLLMQFCdMsy5hYA4JXydS7DQxEf8nnBBCTsQ9QW0b99eioCQS0pKSqCoqEhC0YGRMByAYO7obpvMa5vc0YXBQHUUQDrOckPZvnuThMGBqFB8hS7U6tWrwwIlYCAiD9hKBwMhEBSEgX/GBI5ACEphYaEhBNPp7VutMJY4hKucANwx2w0D1X5GDejocceQD7pZahZ/ncLDmA7IbbffWnFA/vrXv2qlwni0T08TDIIzfPhwKC0thbKyMvmIQjDFxcUGHK073rEJVwu8QMgddvmDu0NqZqThDqlpAlJaTccK3wmKbraYVP3m6n5BCRiIGIpqxX/ZI30eNkIUB3L+/Hk4d+6cobNnzxpgyDEPLY00gFhgMCC27phrdoiEkWkDZAaDke4G0oFrKioCOqRFQNvUmvDx+o/9GoHZ5ZTMNSk+oQQMZNu2bRbxX5L1wVRjREVA8PHChQtQXl4uxcEQFKnSMr/d0Z0DIRgyXNW2usMDpKMCxOSOdAWGAqRDKtOUCHjlg0cd3YIzBcHkk4CBJCUlmWQ3vCUgKCwAL168KKGQCAyH031JhD0QgrFYgWEBouQPG3ckzbCGKy2QND0QVKLQh+s22ILp0KGDTyghA3nllVdMUgs/FQbmhu+++84QgiE43DEoA8ZS/ciqu00y76oLV3PMQDoFE67SGJA0MxCE0T7Frftfr6YFYpdPOvZsZwslYCA9evQwxH/ov1JekkBICAOr8e+//94Qh0KP3DGGM5bahCoPkO48mXtgbMipDyUZjWFzTj1v7rALVzN9hCseqlR3aICg2r5VSwsFBwiBuCRgIF27djXEfygVfNwlly5dMmQHhjtGG6re0cAQ6ipgbJlXHwozo6BwtkcCSOcsa+7o5CkGAwKSFmEbrlQYpAeTa/idT+o3rqOFEjCQHTt2SKm5AytvDgQnDTkQFQoHQ3C+v3jJXHew3JG0KFK4oAGUZkVBkVDhHCYPDFsgKgw1XKX7CFcKEB0MFA17VShr166FqlWr+uWSoHOIOoOrA/LDDz8Y8heOBPPdJThalgsXL1wUoewCFGXHQNG8eCia3wyK5jYREKK9MDIZkFmNzUNdOyDTfeSPNHuHoDsSFRCJqRGmvcG60KWr5ONbxVqgBAxk9OjR+Pi/dkBQOCn4448/moDooKhwdKGsaG4cFL+dCGWrHoeza5+Fsvd7Q/HC1lCYFWOG4ScQn+6YpsBIs8LgQNolR5g2dbd/KwLWbVhrgYL3xZ9cEjCQkSNHmtyBiZuAEBSEwaWCUQHZhrKL56FkaVc498kIKP9iNlzYPQfKd06BsrUDoSinpQCCIMxAdDA6OYWraYpDAnCHy8V32V8mYZB0C1y6UVff5x/lUBoFDOTZZ5+1AOFQsNBTYdhBUV2iAipe1AbObhwKF77Khgu5i6XKxfPzn74BJct7C5c08QIRMM7MbAwdM324Y4bZHUm+3JGmh8H7URr2qW6CgdJNs+Bkph/FYsAtbaalWBQHgsuxqkN08gXn+/JCKPvPE1D+5SwDhgSyJwfOf5YKZWueE8m9uckdZ4RGZN9jdUcGc4cTkKm+3dFqXA1Tk5AEpMBoL8LY6v+s1U6v4NyYummvwoDQpgW8/AGig0NQinOawflPhsOFvQu9QPYKIF8LILumQtn6f4pk/4DJHd/OEM+FfLpDCyTCdmSV6BnqXl3tKqNrC2UHA7X/UK7tZKS6kzJ9+SQO5JNAgJh2jTzwwAMmIPzyxyV2jkEgJYsT4bzIF9wdEgg6ZKdwyDp0SAsJBJ2BMEh8IQqBJNm5w5TQzc44Pi4WWqfUMoBQ+wM+1oiqoofBgKzetcx2IlK3xdXOJX4DwfVwAoLC505XIEB+FCpZ2kWEqxkGCLcWQblI7Oe2vwml7z8uknpTCYPcgTqd3hiKp0VDZ3KHCiTdLlx5gRSMjZNAjo+Lk0B4+0OSCGvGkNcGBo68nsppo52yx5xz/fXXhwWI8Q9S5k00gBAUXxfedH/gIJCizPpQ8k4SlO+aZgJSvmeeyB9T4dzGEVCyqJMY8sbKcPWtB8jp6W4gpwWQ97PreWEEAOQkg3FcPMftpShsgbAUgw5A3t48y3aBC7c5hRUI7hRBINwlOM0e6GUHBSvx4oUJcG7zKOGS2cIV2fIRQ9W5TeOhdPljYoQVb8odHMbpqW6dSYkOKFy5QbhhrHqujqyucTc9yicMBci6z9+z7JK0C1u4Ux83jeug+AUE8wcHQok8mEuFcfHwBxJI0bymUPqfPnBu21g49+mbIkxNFjBGQenKf4i/EzVIRrQpd6hAClKFpsRIJU63wuDuaCeAHB/vhVGlqjvZYmipcl1VODUqLiB3oDbvWWOsOOq2reKmcd5ghAoJCEHxlTsChVKU1cgNJDtaFn+lK/4mCsHnoGz1c1D6779B0fw2InfEanMHd0fBFDeQUykxcPLNWKmiSU1gZUYDWDuzAeS/Hgv5E4UmCDEY1PSDn9yHmtwGeaPj4KjQg6m1AgLy4dqPTGvzum1FFQIEFa6LwpXU3DgonBsvoRQvfFAMg1sLSC0kjMJZHnfM9DhjugeGxh2n3nLDODFZaJJHHIYQuQP7Taj5p3hSMwPG0dfcwgTvLxDcMGG3wRuB4LCZd3zh4z/HPOM3kMvpG5//v2dlDuFAoqOjwwalKKuxnEQsfrcHlK16UrjiMVGxJ0LhnKYyTMlh7kyH3MFheNwhYbyhgUHOGBsru7NQ2J11bEycG8ZrXLFwdFQstHyzlk8Y7ZJrGXu+7FyCQ2iEzxtWUapL7IAY34TFHwEhKLhjPRxX8dvtRX5oAiXv/UXkjglQ/sUsOC9yR9magQJSWzmqOqMm8ukMRpoVhgTCYKhA8BF7T7AhCNvmEAZKhXFEwDgy0i1fQAaIEaC6617nEhwI8XY8XWL3CQRhcCBqQRiaO6KgcF4zWfSVfzVPVOWLRFU+XSTzMVCy5C8GELtQZbgDYSQ7h6rjQmdETsGGIOrSks7wAeOwR05AqE+FNnfr9nkhkBUrVsjeF94rGbRDCMq7774bNiByfWN+c5HEn4Xzwh3lX2aJoW6aqDtGQ8myXnAmo4kZBoWqNAXGW/pQRUAQRsHEOG+X1t13e2GMVmC8ZoVx+F9CI2Jh1Oy7LUD25O00NQ45uQSBYd4iKKiQgeBEYFiBZMdB8ZKH4Kwo/s5tfUO4YyyUfTBQgGov3BFjhSFDlQCR6g5VJ5MZjMl6GBsH1ZdNQdip1bDBPVpnHGEwTCCEDqEEkNP5+2QjETYRUWcXdXUhFNo/rG68IyBr1qwxOopJQQHheQQTes+ePcMDBBeccI0jOx5KFncXCf3vUPqeGOouSIQzs+NF3oi2cQeNqNxAdDBOeGDUb9hANgVh3qtTr4EBgyfxIyxM2cE4NDwW9ubuk41ECOSLL74wWu2oxY7CFrlEN+JCIFwhAUEhkHCMsn48X2DarFCY2UROrxfNaSZCVaweBrmDhaoTSqjaPaK+BIIwYmPjZJcWts5FRdWFY2NVGLFeGKPMIFQYB4WwkQi7u8gl2GqHUKghlVzitGeY2rypB18BcnvAQMJ1lb73iAdGlLHodEbWG9H2eSPN6wyTOwSM+Jh6RncWziRgcykKexlPjIs2wSAgdjAMEAzGwVfdQLAPElvtsP8RXYKhi8IWNaKqUBAGzo3hTACO7LD/HoVQgnYIQcFWgrCEq4yGpvXxM54FJwOEhMFHVO68cUqTxP8nobYMp/ShQSjUNndMVOMSxlgvjCMOzlBdQcr/tkC23Nm5RJdLeF2CxSDmDOy95woZCPaOhwdIIy+MDE2toYQpyhsn1bwhgFDBSkNzfJ34enH2VoVxdLQXBIdxSHHGQeaMA0LYboedwtgDqXOJmkt0oQtrHxxuo6gWChgIWl6FEo4cYoSpDGXC0AYGOsMIU0reoGUBDgZfZ/44JUwxGIcdwhTBOOCBcWBYtGxOpcZU7BTG5M5HXAgEcwkHoroEQxTVQXg4AoLxF0gn3uivAsFEGToQ91JsQDA0SRwTeFRstAkIQVGdcVQDw5czUCfzj8geSHIJb90ml1DYQii6sIXCGgiFR4jg2SttO7fiMK7ya3Jx3opZJiCocFx8CdYEY6o1TNnCmOSdMLw/obXJKfEPtPXpDC0MBsLtjlijMZVcgmGLoKBLKGzRiIsnd16X4CkVKCxQUdOXTw5uthcTZEUB0cKYqnNGjO2koXdtIxbe638X9O4YI95FXa8zXnOGcVAHQ4DYL5Q7pCGcOHFCbgak9m2e3CmX8OTOj/3gQLAwxXNdCEzQ0+8VBcQborwwqAI35wwzjHxljoqv/OV5Cr8fIurB6SFRfsM4oIGBKig4LZtSqa8eXcKTOw9bPLnz6RTKGXiuCwpnDerVqxcaEA4FcwiuhYdyWdY0sMZIcxd8FhhKqNI5w6gzxnhcIYQuCdYZJOwURiDoEgSCLqHk7lQo8rBFOQNnDGjWABU2ILQ5LpSrgK32YYii6ttvZ4wnEBoYr7n1XZyo2l9ubEyHmPIFOWO4HsY3r8RCWd4O2SWMrdvUT8+TuzoE1tUkFLZwlpxmOfADjQoaCAJQoYR6FaR5XJFqhqG6Ip9A2OQMY25KgUHOQJdYkrcfML55Jcboq6deep7cCQgfAusqdwKCRSodTYXC6ZyggYxPH1kBQLwgrDC8zrCDga6wwCAgLEzljYxzQxlhkzOUEEUwzn69zGjbpgMOKLmTS9SwhUDQJbwm6dSpk8wbdP/ww42au2o6h5EX8EY5+oEEBWmHUo+YYCj5Iv8NZ2fIMEUrfWNiTc44zHOGJ0wREIszbGCgqJeeTp2gsEVAyCW6+S0etvBsFxRN69AHOuSdi2g5FQraLtiLTxDmT/ZIB8Izje7OFWZncBg0N2WAGMlClAeKAWO4Mwzc0U+99BS20CUIhJI7r0lotEUu4dPymEfwXtFuTypcgwXi6JJQEvuJZAbjDQUGgRA6Ns6cvHWuOMpgHCLxkZQQXFEHCp6Lks7Y7+SMjalGLz13idNoS5dHeNii05ColQNnESoESLC55FLBbgaCwZiouEIBkTfaHsRhBYQlRA13u8QKwgsDhd3B/MQJyiMUttQ8QmGLikQa/nIg1GlGpyKlLpoYnnaE9FlTLVCCuco2TbS4AgEYIMYTjDgjV6gwjvjhClOIEs44MjwGLtWsZwuD2rX5iRPoEgJCYUsF4jT8XbZsmdGlTC3kIfWHiBdj6xIUJnesOgOzSLEJhIRAIMabHaEFwTYh+HKFmrzRJSoI1MXvLhnt2nioAQfC84g6/OVzW7rJRvUwHgQTEpDU1FTL+ogKJZjkboEwngq8WLcIBgfBYPjrCl2+cENxg9iHMPI3G02n/GwWXdjiQPjclppHaDYYj9tAJSYmSmWvncphNAwYSP/+/aW8J1KnWIAEs4rIQeSN9cgPEIcdQDjB4CHqQov6ANfVkTD2DY0xdQOTQyhsIRBM7E55RK1HaDSVlJRkiMDwD/czzzwTeBfugAEDpJzCFirQK28cg+CRaQirLrGOZPNQ/2IgdCHqVefEjSDQJfjIO4FVh3Ag6BJdPcLzCCV2DE8cBmnGIvPhCy+99FJ4gCTPH2cBgi82ICAEgUAoS6vqlhzLpKAKwocrOAxyBkJRgaDocBynekSdRuEFIt78jh07WoDwezhq1CgXKuiQxcOWnUsCySVHR8eYhq5HlApb3Y5jG5oIhA9XfMNAoM7tXgbw4TaAYSkmIPwoKbvErgLhBSKCQRhcKgwU9v97zgAIvE+dZLLbqBdCCl15E5rLsGQHAXXQXxCv6os8Oxhfv1jPaDbVucQOCM1r8QKRr7VjyFJhoGavMp8sN3ToUBcpJIc4uYRmhP2d3/rh3FEtiIMaRxzQ5QgFhB0MDoLEu3/h3+sBrq1ncYmaR9ShL19FpEZYHqYIRs9HHtaGqqBDFneI6pJQEzxP0gYEnRMcQPgTnrh4BzD1yEuXiNfDHcILRMoj6BCajqfETkB4eOKPyv3aN2zYMBdXyEBUKCMmvWybT+SbdQLCEvSB4TbiEF5VIfgPwg0DtEDkBnIBRc0jupGWCgRHWrowpYEBkyZNcqkKepSlytRD0qJ5UE6xc4EFQgiO4M5wOkkCGnaHHzZs8zuxU4HIw1OgMIIConOIv6Fr0KBBzlPwOf+wB6B1hE2y9gFDbTRVz12hpI4uUYFQxc4Te69evWTx5y+M5ORkl50CBjJw4EBb+QOFwhe+Md3l2wm+R02+YOjasbVHRoGIaa5ILRCe2DF86Qo/hDF//Qy/YQQFxM4hOqdMWTjBFgq+IS0QvPkEYJjn5g+LCRpCLpNdO7bTGV7guhMuikcdEMojNA3iVPihsrOzXb4UVofonDLgpadtoWAIS0lJsdwo3c0PJCRZYLwc7fPAArtjojCxY+jiIy0Uzk1h4YcThASEg1mwerYJxpIlS1z+KOQ6RCf1k/GWZmqFr6HgGjO/9r5Y1wpiaIAQPNo3tJFfBxY4AVFHWgsXLpTr4TRjSyIg89anq+54df369S5/VCFAdFCccgofhdF0i78A7ECg9v6znt9HeqhhS63WeR6hs11QKhTd+/YXRoUCsYPSuXtHn2BEcvMbSq6NLuQuD/jgGx0QhEFrPrjcyk/t5otNqFBA/CRA7MBMWzbJEQjdABVKrp8K9hQibYEoLlpq5efaczCaVT9sO3BVWiBPPfVUUCGMNk74C+Lw5C4hHQ3FgfTt29d00iqdSayCGTzsRcv72rJli6vSA/Gshlle/OxVb/kFpXmz5nBgmCZPDI0L+QQivKgpFBsy1aNvORQORvd+tm7d6vrFAMH/o8out/hyjNokRMJRjRguemeNxSfcrsUO2/F69+6tBUIztHSGJEFRweCf7V4//veyv0gg/fr1cz399NO2YFq2SggYDG/V5j30K1euNIDQxmYEox7Cxo8rVMGgBgx6xhYEFnTbt293/eKBeMLYKbs3OuPfk4NyjQ4OdeRy8R5EFQ5BsXttHt2ckZHh+lUBwZliT9KPd3rz/fo/HjAUHRg7QCqY6e++6QQidtasWRLArxaIGNU41i+qhk0Yot3wHQwggpLQ0tkRgwcPdo0ZM8aVmZnp+k0BwT/r/is+f4SdrMk5Y6FTt46OYBJEnkLX+fMz09LS5ExspQTyM2pXMIBC1M/+viszEFWX/1oh/FKBOIGa+ksFYAfk/wFgc1ShfvacmQAAAABJRU5ErkJggg=='

# -------------------------------------------------------
# Reverses endian. Ex: "hello!" = "o!llhe"
def reverse_endian(hex):
    final = ''
    i=0
    while i < len(hex)/2:
        final = (hex[i*2] + hex[i*2+1]) + final
        i = i + 1
    return final

# Returns string with flp hex time
def get_hex(track):
    track.parse()
    track = str(track)
    idx = track.find('(ProjectTime) =') + 16
    return track[idx:idx+48]

# Cleans string and converts to float
def clean_convert(hex):
    hex = hex.strip()    # remove any lingering returns
    hex = hex.replace(" ","")     # remove all spaces
    hex = reverse_endian(hex)
    hex = hex[0:16]
    return struct.unpack("d", struct.pack("Q",int("0x"+hex, 16)))[0] # convert hex string to float!

# cleans string for time conversion
def hex_time(hex):
    hex = hex.strip()    # remove any lingering returns
    hex = hex.replace(" ","")     # remove all spaces
    hex = reverse_endian(hex)
    hex = hex[16:32]
    hex = struct.unpack("d", struct.pack("Q",int("0x"+hex, 16)))[0]
    return datetime(1899 ,12,30) + timedelta(days=hex)

# MAIN-----------------------------------------------------------
if __name__ == "__main__":
    # Define window layout
    sg.theme('Dark')
    layout = [[sg.MLine(size=(54,17), key='-ML-', disabled = True, write_only = True, no_scrollbar = True, auto_refresh = True)],
                [sg.Text('Select Time Frame (Leave blank for all time)')],
                [sg.In('Earliest',disabled = True,text_color = '#737373',size=(23,1)), sg.Text(' to '),sg.In('Latest',disabled = True,text_color = '#737373',size=(23,1))],
                [sg.CalendarButton('Start Date', target=(2,0), key='date1'), sg.Text('                             '),sg.CalendarButton('End Date', target=(2,2), key='date2')],
                [sg.Text('')],
                [sg.Text('Select Master Folder')],
                [sg.In('No Folder Selected',disabled = True,text_color = '#737373'), sg.FolderBrowse(initial_folder = 'C:',key = "SelectedFolder")],
                [ sg.Button('About',button_color='#52829c'), sg.Text('                     '), sg.Button('Calculate!'), sg.Text('                          '), sg.Text("v0.3.0",text_color='#a1a1a1')]
             ]

    # Create WINDOWS
    window = sg.Window('FL Studio Time Calculator', layout, grab_anywhere=True,icon=ico)

    # GUI Loop
    while True:
        event, values = window.read()   # Read the event that happened and the values dictionary
        if event == sg.WIN_CLOSED:     # If user closed window then exit
         window.close()
         break

        if event == 'Calculate!':
            if values[2] == 'No Folder Selected':
                sg.Popup('Error, no folder selected', keep_on_top=True)
            else:
                if values[0] == 'Earliest':     # Grabs Earliest inputed date
                    date2 = date(1997, 12, 18)
                else:
                    date2 =  datetime.date(datetime.fromisoformat(values[0]))

                if values[1] == 'Latest':       # Grabs latest inputed date
                    date1 = datetime.date(datetime.now())
                else:
                    date1 = datetime.date(datetime.fromisoformat(values[1]))
                window['-ML-'].update('')
                if(date2 > datetime.date(datetime.now())):
                    print("     ----------------------------------------------")
                    print("     ",date2, " Hasn't Happened Yet!")
                    print("     ----------------------------------------------")
                elif(date2 > date1):
                    print("     ----------------------------------------------")
                    print("     Make Sure Start Date Is Before End Date")
                    print("     ----------------------------------------------")
                else:
                    total = 0   # will store total time
                    totalfiles=0    # Store total files
                    earliest = None     # Store earliest project date
                    latest = None       # Store latest project date

                    everything = glob.glob(values[2]+"/**/*.flp", recursive=True)
                    if not everything:                              # Checks if list is empty, no flps found
                        sg.Popup('Error, no FLP files found', keep_on_top=True)
                    else:
                        print("Scanning",values['SelectedFolder'],"for project files. This may take a moment!")
                        directory = values[2].replace("\\","/")
                        for thing in everything:        # for every "flp" file
                            thing = thing.replace("\\","/") # idk why this isnt already happening within glob
                            x = FLPFile(thing)
                            x.parse()
                            for idx, track in enumerate(x):
                                track.parse() # this sucks
                                window['-ML-'].update("Found file: "+thing.replace(directory+'/',''))   # Clear GUI console
                                print("\nTotal found: "+str(totalfiles))
                                hex = get_hex(track)                                                    # Finds Project Timecode Hex
                                cur = datetime.date(hex_time(hex))                                      # Finds creation date of file

                                if cur >= date2 and cur <= date1:                                  # If project dates lands between user inputed date
                                    if earliest == None or cur > earliest:                              # If current project date is newer than earliest date
                                        earliest = cur

                                    if latest == None or cur < latest:                                  # If current project date is older than latest date
                                        latest = cur

                                    total += clean_convert(hex)                                         # Extract project time
                                    totalfiles+=1
                                del track           # clear parsed memory
                            del x               # Close FL file

                        window['-ML-'].update('')                               # Clean GUI console
                        if totalfiles == 0:
                            print("     ----------------------------------------------")
                            print("     No Project Files Found Within Date Range :(")
                            print("     ----------------------------------------------")
                        else:
                            # Stats calculations
                            total = str(total)
                            days = total[0:total.find(".")]
                            hours = str((86400 * (float(total) - float(days)))/3600)
                            totalhours = str(float(days) * 24 + float(hours))
                            totalhours = round(float(totalhours),2)
                            temp = hours
                            hours = hours[0:hours.find(".")]
                            min = (float(temp) - float(hours))*60
                            min = round(float(min),1)
                            averagehours = str(round(float(totalhours)/float(totalfiles),2))
                            averagedays = earliest-latest
                            averagedays = round(averagedays.days/totalfiles,2)

                            print()
                            print("     Howdy",os.getlogin()+"!")
                            print("     It is",date.today())
                            print()
                            print("     Your FL Studio Stats For ", date2 , " to ", date1)
                            print("     ----------------------------------------------")
                            print("     Total Project Files:",totalfiles)
                            print("     -")
                            print("     Total Active Time:",days,"day(s),", hours,"hours, and",min,"minutes!")
                            print("     -")
                            print("     Total Active Hours:",totalhours)
                            print("     -")
                            print("     Average Hours Per Project:",averagehours)
                            print("     -")
                            print("     Average Days Between New Projects:",averagedays)
                            print("     ----------------------------------------------")
                            window.Refresh()
        elif event == 'About':
            layout2 = [[sg.Text('Developed by: Elliott Chimienti & Zane Little')],
                        [sg.Text('FL Studio keeps track of how many active hours you spend on each project, but not your total time in the program. \nWith this application, you can finally see your total hours without having to open up all your files and adding everything together! \nIdle time is still not accounted for, so the time this program displays to you only shows your active working hours. \nYou may also select dates for the program to search between, say, if you wanted to see how many hours you spent on FL in a given month (or whatever time frame you like)!\n')],
                        [sg.Text('This program was created out of the primal, human urge to keep track of and gawk at the amount of time we all spend on FL Studio. \nFor better or for worse, we will never stop producing!')],
                        [sg.Button('Support Us!',button_color='#d1b000'), sg.Button('Exit')]]
            pop = sg.Window('About', layout2, grab_anywhere=True, icon=ico)
            while True:
                event2, values2 = pop.read()
                if event2 == sg.WIN_CLOSED or event2 == 'Exit':     # If user closed window with X or if user clicked "Exit" button then exit
                    pop.close()
                    break
                elif event2 == 'Support Us!':
                    webbrowser.open(r'https://ko-fi.com/flhourcounterguys')
                pop.refresh()
