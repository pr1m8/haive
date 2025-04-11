# Fix this
"""
haive-py3.12will@DESKTOP-JM28UET:~/Projects/haive/backend/haive$ python3 -m src.haive.core.toolkits.gradio_toolkit
Traceback (most recent call last):
  File "<frozen runpy>", line 198, in _run_module_as_main
  File "<frozen runpy>", line 88, in _run_code
  File "/home/will/Projects/haive/backend/haive/src/haive/core/toolkits/gradio_toolkit.py", line 9, in <module>
    StableDiffusionTool().langchain,
    ^^^^^^^^^^^^^^^^^^^^^
  File "/home/will/Projects/haive/backend/haive/.venv/lib/python3.12/site-packages/gradio_tools/tools/stable_diffusion.py", line 28, in __init__
    super().__init__(name, description, src, hf_token, duplicate)
  File "/home/will/Projects/haive/backend/haive/.venv/lib/python3.12/site-packages/gradio_tools/tools/gradio_tool.py", line 36, in __init__
    self.client = grc.Client(self.src, hf_token=hf_token)
                  ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/will/Projects/haive/backend/haive/.venv/lib/python3.12/site-packages/gradio_client/client.py", line 142, in __init__
    raise ValueError(
ValueError: The current space is in the invalid state: RUNTIME_ERROR. Please contact the owner to fix this.
haive-py3.12will@DESKTOP-JM28UET:~/Projects/haive/backend/haive$ 
"""
from gradio_tools.tools import StableDiffusionTool,\
    ClipInterrogatorTool,ImageCaptioningTool,ImageToMusicTool,\
    WhisperAudioTranscriptionTool,\
    StableDiffusionPromptGeneratorTool,TextToVideoTool,\
    DocQueryDocumentAnsweringTool,BarkTextToSpeechTool,\
    SAMImageSegmentationTool

gradio_toolkit = [
    StableDiffusionTool().langchain,
    ClipInterrogatorTool().langchain,
    ImageCaptioningTool().langchain,
    ImageToMusicTool().langchain,
    WhisperAudioTranscriptionTool().langchain,
    StableDiffusionPromptGeneratorTool().langchain,
    TextToVideoTool().langchain,
    DocQueryDocumentAnsweringTool().langchain,
    BarkTextToSpeechTool().langchain,
    SAMImageSegmentationTool().langchain
]
print(gradio_toolkit)
