# Boss_MayaTools
mayaで使えるpythonスクリプト。
主にアニメーション関連で役立つスクリプトを公開します。

# ツール一覧
<b>・BakeFramer.py（MAYA）</b><br>
＞任意の間隔でアニメーションキーを打ってくれるスクリプト。削除したくないフレームも指定可能です。<br>
BakeFramer.pyをdocument/maya/scriptフォルダに保存し、以下のスクリプトをmayaでのスクリプトエディタ（pythonのほうに）で入力してください。<br>
<pre>
  <code>
    import BakeFramer<br>
    BakeFramer.create_gui()
  </code>
</pre>
<b>・AnimMirror_tool.py（MAYA）</b><br>
＞今のところMoxリグ専用。アニメーション反転ツール。<br>
AnimMirror_tool.pyをdocument/maya/scriptフォルダに保存し、以下のスクリプトをmayaでのスクリプトエディタ（pythonのほうに）で入力してください。<br>

<pre>
  <code>
    import AnimMirror_tool<br>
    AnimMirror_tool.mirror_tool_gui()
  </code>
</pre>

# 利用条件
・このスクリプトの再配布、転売を禁止します。
・著作者（BossHachi）への報告、クレジットの記載なしに商用利用していただけます。
・このスクリプトに関する著作権は著作者である（BossHachi）が 保有します。
