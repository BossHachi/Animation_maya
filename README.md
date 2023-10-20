# Boss_MayaTools
mayaで使えるpythonスクリプト。
主にアニメーション関連で役立つスクリプトを公開します。

# ツール一覧
・BakeFramer.py（MAYA）
＞任意の間隔でアニメーションキーを打ってくれるスクリプト。削除したくないフレームも指定可能です。
BakeFramer.pyをdocument/maya/scriptフォルダに保存し、以下のスクリプトをmayaでのスクリプトエディタ（pythonのほうに）で入力してください。
import BakeFramer
BakeFramer.create_gui()

・AnimMirror_tool.py（MAYA）
＞今のところMoxリグ専用。アニメーション反転ツール。
AnimMirror_tool.pyをdocument/maya/scriptフォルダに保存し、以下のスクリプトをmayaでのスクリプトエディタ（pythonのほうに）で入力してください。
import AnimMirror_tool
AnimMirror_tool.mirror_tool_gui()


# 利用条件
・このスクリプトの再配布、転売を禁止します。
・著作者（BossHachi）への報告、クレジットの記載なしに商用利用していただけます。
・このスクリプトに関する著作権は著作者である（BossHachi）が 保有します。
