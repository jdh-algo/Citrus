import re 


prefix = "You are an expert with extensive experience in medical research and clinical practice, and you are needed to assist users in answering questions related to medical issues. Let's think step by step."
prompt_template = """You are tasked with addressing a medical examination question. Please carefully read the question, provide a detailed thought process, and then present your final answer.

Here is the question:
<Question>
{question}
</Question>

Please begin your response.

The formatted output should be as follows:
<think>
[Insert Your Detailed Thought Process here]
</think>
<answer>
[Insert Your Final Answer here]
</answer>"""

## 特殊符号
s_invalid_special_tokens={'<Answer>','</Answer>','<Thoughts>','</Thoughts>','<Conclusion>','</Conclusion>','<Experience>','<Ground Truth>','<Question>','</Question>','</Experience>','<总结>','<Reasoning>','</Reasoning>','<Final Answer>','</Final Answer>'}
s_invalid_special_tokens|={'<Answer>','</Answer>','<Thoughts>','</Thoughts>','<Conclusion>','</Conclusion>','<Experience>','<Question>','</Question>','</Experience>','<Final Answer>','<Ground Truth>','</Final Answer>','<总结>','<Final Answer: Atorvastatin>','<Reasoning>','</Reasoning>','<Reflection>'}
s_invalid_special_tokens|={'<|im_start|>'}
s_invalid_special_tokens|={'<Thoughts>','</Thoughts>','</Answer>','<Answer>','<Conclusion>','</Conclusion>','<Experience>','</Experience>','</Question>','<Question>','<Output>','</Output>','<head_glance>','<!DOCTYPE html>','<html lang="en">','<head>','<meta charset="UTF-8">','<title>','</title>','</head>','<body>','<h2>','</h2>','</body>','</html>','<Conclusion hidden>','<missing_text>','<HIGHLIGHT>','</HIGHLIGHT>','</Explanation>','<pre>','</pre>','<Reflection>','</Reflection>','<QuestionTopic>','</QuestionTopic>','<Interdenga intubation, surgeries>','<Conclusion:>','<Reasoning>','</Reasoning>','</thoughts>','</Thouths>','<meta>','</meta>','<Solution>','<Experience的信任度>','<Tought>','< Conclusion >',}
s_invalid_special_tokens|={'<p>','</p>','<Experience deepened>','<Displacement>','</An بدأ>','<PointERT>','</PointERT>','</br>','</ Answer>','<Answer">','<TransportMedium>','</TransportMedium>','<Next Step>','<GCoT>','</GCoT>','<Conclusion Reasoning>','<SARI>','<Val>','</Val>','<Experience锦标 collect>','</s>'}
s_invalid_special_tokens|={'</Extract>','</Task>','</Data>','<sub>','</sub>','<Summary>','</Summary>','<Experience and Ground Truth>','</Experience and Ground Truth>','<br>','</Conclusions>','</Conclusion hidden="true">','<Fact>','<1 or >','<div>','</div>','<Experience content>','</Experience content>','<Title>','</Title>','< Mode\n- Mode >','<Explanation>','<Conclusion type="elaborate">','<Conclusions>','<Final Thought>','<ExperienceCurve>','</ExperienceCurve>','<StudyDesigns>','</StudyDesigns>','<Reflect>','</Reflect>','</span>','</Conclusion：>','<experience>','</experience>','</Thought>','<Conclusion ref_number="">','<Conclusion snippet>'}
s_invalid_special_tokens|={'<Answer >','<Body>','<?xml version="1.0" encoding="UTF-8"?>','<img>','</legend>','<Wait>','</script>','<h1>','</h1>','< conclusion>','</BlockingOutput>','<g>','</Architecture Emoji: >','</Upload>',"<Medical Expert's Final Answer>",}
s_invalid_special_tokens|={'</sup>','<sup>','<your answer>','</strong>','<strong>','<Thought>','< 0 \\) and \\( f(1.8125) >','<u>','</u>','<stdio.h>','<你的答案>','<MISSING CONDITION>','< 100,000 \\mid X >','</i>','<li>','</li>','< nobr aria-hidden="true">','<i>','<Antimicrobial drug>','< 0.1 \\) for \\( t >','<Answer GWL>','</Answer GWL>','<AnswerPAIRA>','<1,2>','<2,4>','<5,4>','<5,6>',"<%= ['celiprolol'] %>",'</button>','<script src="script.js">','</answer>','< span class="mord">','<AnswerEigen>','</AnswerEigen>','<br/>','<Answer(INVOKESkeletonDecision)>','<String>','</String>',"<Answer Fracrben's Syndrome>",'<html>','<Al>','</Sentence>','<Answer实施细则>','<stdlib.h>','<Point>','</Response>','<References>','<您的答案>','<Answer ":”>','<Answer标志>','<Answer\n   \n  >','<Answer圈套>','</Answer圈套>','<int.STL style="color: red;">','</int.STL>','<50mmHg，PaCO₂>','<Answerphabet>','</Answer >','<Answer贾>','< Answer >','</ Answer >','<Answer Aware>','<Answer QMainWindow-Innermost>','</Answer QMainWindow-Innermost>','<Agent>','<copy Code>','</copy>','<div id="result">','<!-- The result will be displayed here -->','<script>','<ul>','</ul>','<a href="https://naruto.fandom.com/zh/wiki/鸣人" target="_blank">','</a>','<button onclick="generateceleb()">','<div id="celebContainer">','<h1 id="heading">','<button onclick="addPerson()">','<div id="celebList">','</答案>','</>','<quote>','</quote>','<Answer=A Krukenberg tumor/>','<Enzyme Group>','<Answer.Retrofit>','<Answerstrain content here: -->','<?=$unknown$>','< span class="mord mathnormal" id="MathJax-Span-83">','</ span>','< span class="msupsub">','< span id="MathJax-Span-84" style="margin-left: 0.228em;">','< span style="display: inline-block; position: relative; width: 0.358em; height: 0px; font-style: normal; vertical-align: 0px;">','< nobr aria-hidden="true" style="position: relative;">','< span style="position: relative; top: -1em; margin-right: 0.1em; display: inline-block;">','< span style="display: inline-block; height: 1.111em; clip: rect(1em, 1000em, 2em, -1000em); overflow: hidden; vertical-align: -1em;">','< span style="display: inline-block; width: 2em; height: 1em; clip: rect(0em, 2em, 1em, 0em); overflow: hidden;">','<PRESIDIO_ANONYMIZED_EMAIL_ADDRESS>',"<Answer'^^>","</Answer'^^>","</Answer'>",'<Answeränger>','</Answeränger>','<Answer filament="true" expression方位="positive">','<Answer Dysfunction>','</Answer Dysfunction>','<Answer CGPoint="false" Range="not_specified">','<Answerטו>','</Answerטו>','<IActionResult?>','<Answer ticket>','<Answer/aws-translated>','</Answer/aws-translated>','<internal_matrix_table>','</internal_matrix_table>','<Answer勃肯特>','</Answer勃肯特>','</Answer/>','</Answercents>','<Answer globalsyndromes.org/gilbert-syndrome />','<Answeriteration>','</Answeriteration>','<label>','</label>','<a>','<Answer*(-_*)>','<Answer锦标>','<Answer Consent>','</Answer Consent>','</Knowledge>','</Assistant>','<Answer QAction="C">','<Answer Inferential>','<Answercompiled>','</Answercompiled>','<Answer-final>','</Answer-final>','<Answer/XML>','<Answertsx>','<meta http-equiv="X-UA-Compatible" content="IE=edge">','<meta name="viewport" content="width=device-width, initial-scale=1.0">','<!-- Custom CSS -->','<Answer.Health>','</Answer.Health>','<Answer=Rosacea>','<intersection>','</intersection>','<工作安全性>','<-Answer>','<Answer⁻¹>','</Answer⁻¹>','<Answer./(.)>','<Answer Fragile X Syndrome>','</componentStackAdditions>','<! Answer>','<! /Answer>','</section>',"<!-- Durck's Staining -->",'<Answer=#7FFFD4>','<Answer舊>','</Answer舊>','<Your answer>','<Answerkilancellor>','<em>','</em>','<G函数名>','</Knowledge-point>','</Strategy>','<Resource:conjtgions>','<心力衰竭>','<Passage>','</Passage>','< Answer>','<AnswercalculatorRON>','<您的回答>','</References>','<Question type="some_type">','<Question type="学术">','<Question type="教育">','<Question type="测试">','<Question type="操作">','<Question type="其他">','<windows.h>','<tchar.h>','<IF="xx...">','<ELSE="xx...">','<iostream>','<fstream>','<Answer全流程>','</Answer全流程>','<Condition>','</Condition>','</installation>','</Video>','<coverage>','</same>','</Address>','<strong_Cancelled>','</fullName>','</system>'}
s_invalid_special_tokens|={"""<Thought>""","""</user>""","""</Thought\n\n">""","""</Answer\n>""","""</Answer\n">""","""</thought>""","""</chat-turn>""","""</User>""","""</Thought\n\n>""","""</ Thought>""","""</Output\n>""","""< Output>""","""</system>""","""</Doc>""","""<file>""","""</Answer\n/>""","""<text>""","""</Answer\n?>""","""</details>""","""<li>""","""</li>""","""<html>""","""<key>""","""<name>""","""<!-- Output -->""","""</Input>""","""<details>""","""<summary>""","""</Thought >""","""<string>""","""</Output/Runtime>""","""</Session>""","""</document>""","""</Thought\nenes, particularly albumin, patients often develop hypoalbuminemia, which means low levels of albumin in the blood. This makes sense because if a lot of protein is being lost in the urine, there's less protein circulating in the blood.\n\nThe low albumin levels lead to reduced oncotic pressure in the blood vessels, causing fluid to leak out into surrounding tissues, resulting in edema. So, edema is another major feature. Patients with nephrotic syndrome can have puffy faces, swollen ankles, and even abdominal swelling due to ascites.\n\nAdditionally, there's hyperlipidemia, which includes high cholesterol and triglyceride levels. This seems a bit indirect, but it's a well-documented feature. The liver increases lipid production in response to the low albumin levels, leading to high cholesterol and other lipid abnormalities.\n\nWait, let me think again. What else is associated with nephrotic syndrome? Hmm, it's also known to increase the risk of thrombosis and infections due to the loss of various proteins, including anticoagulants and immunoglobulins, in the urine. However, these are complications rather than primary characteristics.\n\nSo, let's list out the key features again to make sure I haven't missed anything:\n1. Proteinuria (>""","""</Answer\n/XML>""","""</output>""","""</Answer\n Vitamin D acts as a hormone through its active form, calcitriol, which regulates calcium levels and influences gene expression, fitting the definition of a hormone.\n\n\nVitamin D\n\n>""","""</Answer\nWait, that doesn\'t seem right. Based on the detailed thought process, the correct storage duration for red blood cells at 4°C is indeed 21 to 35 days, depending on the additive used, not up to 42 days. The 35-day threshold is achieved with CPDA-1 solutions containing adenine. Therefore, the final answer should be "Up to 21-35 days."\n\n>""","""</Answer\n)">""","""</Answer\npageNum="1" num="9451" diffCount="1" hasDiff="true" Longitia="2023-10-12T06:34:16.9075467+00:00" Acallonia="2023-10-12T06:34:16.9075467+00:00">""","""<strong>""","""</strong>""","""</summary>""","""</Answer\nwelcome_rotation>""","""</Answer\n\n\n\n\n\n\n>""","""<Term>""","""</Term>""","""</Thought uneasy>""","""<Ragged red fibers>""","""</Response>""","""</Answer\n()>""","""</Answer\n**\n\n\nThe reasoning provided is logically sound and correctly identifies the timeline of infections post-transplant, associating them with the levels of immunosuppression. The intermediate phase, particularly one month post-transplant, aligns with an increased risk of viral infections due to high immunosuppressive therapy. The reasoning accurately highlights the significance of infections like CMV and polyomaviruses and acknowledges the possibility of bacterial and less common fungal infections. This approach is consistent with established medical knowledge and effectively addresses the question at hand.\n\nFurther thought could be given to specific prophylactic strategies, such as antiviral prophylaxis for CMV, which is commonly used in transplant recipients. Additionally, considering personalized immunosuppressive regimens could provide more nuanced insights into infection risks.\n\nOverall, the reasoning comprehensively covers the types of infections to expect and the context in which they occur, contributing to a well-rounded understanding of the post-transplant infection landscape.\n">""","""</Answer\neducted text">""","""</Thought\n\n-Pack name="Medical Examination" author="Dr. Emily" description="A collection of questions and answers related to medical examinations and anatomy." difficultyLevel="Intermediate" version="1.1" date="2023-10-10">""","""</Answer\nwarz\n\n ">""","""<Tктив>""","""</Тктив>""","""<!doctype html>""","""</output格式>""","""<Doc>""","""<?xml version="1.0" encoding="UTF-8" ?>""","""</dd>""","""</OutputBlock>""","""</Answer\n/">""","""</Thought doença>""","""<div class="output_subwindow">""","""</Answer\nmunition>""","""</Answer\n;">""","""</Thought\n)>""","""</output quarry>""","""</Answer\n()">""","""<search>""","""<reason>""","""<url>""","""<short_task_desc>""","""<command_names_for_GPT_Agent>""","""<prompt>""","""<message>""","""<list_of_suggestions>""","""<full_code_string>""","""</ul>""","""</Answer\n)>""","""</thought\n>""","""<!-- Format the output to just present the final answer:\nThe schedule for HDCV in rabies post-exposure prophylaxis (PEP) is as follows:\n\nFor **unvaccinated individuals**:\n- Day 0: First dose of HDCV and administration of rabies immunoglobulin (RIG)\n- Day 3: Second dose of HDCV\n- Day 7: Third dose of HDCV\n- Day 14: Fourth dose of HDCV\n- Day 28: Fifth dose of HDCV\n\nFor **previously vaccinated individuals**:\n- Day 0: First dose of HDCV\n- Day 3: Second dose of HDCV\n\nThis schedule ensures both immediate and long-term protection against rabies, appropriately adjusted based on prior vaccination status.\n-->""","""</Internal Thought>""","""</Answer\nPlugin outlier detected: extraneous characters found. Please check formatting.">""","""</ドレス>""","""</ Output>""","""</Answer\ntypo>""","""</Answer\n的商品">""","""</Thought\n\nAlright, after thoroughly considering these aspects, Burkitt's lymphoma is positive for B-cell markers (CD19, CD20, CD10), the MYC translocation, high Ki-67 proliferation index, and often EBV markers. This comprehensive breakdown should provide a clear understanding of the key positivity markers for Burkitt's lymphoma.\n\n>""","""<'EOT'\nThe gold standard investigation for pulmonary embolism is pulmonary angiography due to its definitive and detailed visualization of blood clots in the pulmonary arteries. However, in clinical practice, CT pulmonary angiography (CTPA) is commonly used for its high sensitivity and specificity, non-invasiveness, and widespread availability.\nEOT;\n\necho formatOutput($thought, $answer);\n?>""","""<div style="page-break-after: always;">""","""</OutputFormat>""","""</OutputPropertyParams>""","""</Answer\nipsis'>""","""<meta name="description" content="Detailed reasoning about ribosome recycling in bacterial translation.">""","""<meta name="keywords" content="ribosome, recycling, translation, prokaryotic cells, tRNA, ribosome subunits">""","""<meta name="author" content="OpenAI">""","""</Asset>""","""</Thought\n\nThe intercostal nerves are branches of the anterior rami of the thoracic spinal nerves (T1-T11). Each intercostal nerve corresponds to the intercostal space below its originating thoracic level. The T12 spinal nerve gives rise to the subcostal nerve.\n">""","""<div class="outer_container">""","""<b>""","""</b>""","""<!DOCTYPE markdown>""","""</markdown>""","""</suggestion>""","""</Answer\n**仲**>""","""<Nutherford_Summary>""","""</ Question>""","""</Answer\n_Portfolio>""","""</Portolio>""","""</OutputStatus>""","""</Thought\n\nFinally, the activator for self-cure resin is typically an amine component, which works with a peroxide or another free radical initiator to start the polymerization process.\n>""","""</innerThought>""","""</Thought\n\nOkay, let's break down the question further to ensure we cover all relevant aspects of nephrotic syndrome.\n\nNephrotic syndrome is a kidney disorder characterized by heavy proteinuria, hypoalbuminemia, hyperlipidemia, and edema.\n\nWait, let me think again. Considering these main features, we need to explore what might NOT be true for nephrotic syndrome.\n\nFirst, let's list common findings in nephrotic syndrome:\n- Heavy proteinuria (>""","""<$Output>""","""</ Consent>""","""</Answer\n(strposinesece)>""","""</Answer\nนับ\n">""","""</python>""","""</Thoughts\n\nAlright, the adverse effect of levodopa not blocked by carbidopa is centrally mediated, particularly dyskinesias and other central side effects like psychiatric symptoms.\n">""","""<AOutput>""","""</AOutput>""","""</thought >""","""</Answer\n얍\n>""","""</Answer\n'>""","""</Answer\nacency detection: High similarity between generated answers, suggesting a consistent understanding of the requirements of RNA polymerase.\n\n>""","""</Thought ?>""","""</Answer\n\\">""","""</Assistants>""","""</src>""","""</Output\n">""","""</Answer\n typography50">""","""</s-poem>""","""</Sound>""","""</Answer\n\u200b>""","""</Answer\n-grey-">""","""</ft想想>""","""</Answer\nVirgin_MATERIALS">""","""<br/>""","""<\\Answer>""","""</Thought\n\n?>""","""</Answer\nADIUS="0.5em">""","""</ videogpt>""","""<EM>""","""</EM>""","""</тельt>"""}
s_invalid_special_tokens|={'<sstream>','<KeySearch>','<Answercapitalize>','<Answer*bupropion*Answer>','<Strong>','</Strong>','<UFunction of Analysis>','<Answer))/>','<!-- due to its association with the blood-brain barrier -->','<severity_strand>','<Answer₀>',"<Answerexpiration'>",'<AnswerCTIONS>','</AnswerCTIONS>','<Answer ALL ABOVE CONDITIONS>','</Answerqrst>','<Text>','<PRESIDIO_ANONYMIZED_PHONE_NUMBER>','<font color=red>','</font>','<医德>','<Answer-city>','</Answer-city>','<Answer_part>','</Answer_part>','<Answer worn bone scan>','<Answer nuova voce>','<link rel="stylesheet" href="https://example.com/assets/css/gray-acadia.css">','<div class="Knowledge-Lookup dark-mode">','<Answer Marc than 5 words>','<$Thought>','</$Thought>','<尿pH值多为碱性>','<AnswerDATABASE>','</AnswerDATABASE>','</ThoughtAndAnswer>','<a href="https://www.flickr.com/photos/enifting-scuola-epsom/">','<a href="https://creativecommons.org/">','<MHC分子和抗原>','<ucarousel>','</ucarousel>','<Answerisspace />','<Ref>','</Answer*>','<Answer Presenter>','</Answer Presenter>','</Income>','<sub/interface>','<callback>','<Answer-payment>','<Answer José>',}
s_invalid_special_tokens|={'<|start_header_id|>','<output>','<|end_header_id|>','<|python_tag|>','<thought>','<|reserved_special_token_89|>','<Thread>','<|reserved_special_token_15|>','<nanswer>','</nanswer>','</answer output>','<len linea>','</len linea>','<Memo>','</Memo>','<|reserved_special_token_99|>','<baseoutput>','</baseoutput>','</Point>','<\\Thought>','<()>','<?=$_RST?>','<80 fL), or macrocytic (>','< boost swagger -->','<table>','<thead>','</thead>','<tbody>','</tbody>','</table>','< 5 \\)\n   - \\( v >','< 5 \\), \\( v >','<->','<task>','</task>','<activity>','</activity>','<Assessment>','</Assessment>','</thin>','<llink>','</llink>','</Style>','<results>','</results>','<RichOutput>','</RichOutput>','<answerahoma>','</answerahoma>','<ATP>','</solution>','<small>','</small>','</Thinking>','<5D60>','</5D60>','<number>','</ thought >','< output >','</Question كيلعبمر>','<Variable>','< Question >','<?formatlongDate">','<select>','</select>','<question>','</question>','<create>','<Short answer>','</Short answer>','<input point>','<output point>','<|reserved_special_token_22|>','<*Anopheles culicifacies*>','<areafed>','</areafed>','<floatobjc ellipsis>','<thibsecurity>','</thibsecurity>','<Output >','<!--[ично-->','<!--fclose-->','<$user>','<hink>','<num>','</num>',}
s_invalid_special_tokens|={'[Insert Your Detailed'}
s_invalid_special_tokens|={'<T>','<E>','<Array eskort_${bytesTRGL}>','<actic bigep>','<|结束_header_id|>','<Student>','</Student>','</Main RECE>','<Type of Economy>','<Benefit for Businesses>','<Issues for Gig Workers>','</_selector>','<Option_secure环境>','<UN...">','<|reserved_special_token_47|>','<Esox lucius>','</host>',}
s_invalid_special_tokens|={'<answer>','</answer>','<think>','</think>','</ charity>','</history>','<EdgeType>','</ charter>','<Option>','</Option>','</detail>','</capacity>','<kip2>',}
s_invalid_special_tokens|={'</Think>','<Think>','</as>','<Thinks>','</Thinks>','<Outputs>','</Outputs>','</options>','<Thinking>','<Tdata>','<displays>','</displays>','</Tdata>','<result>','</result>','<len>','<!--EndFragment-->','<Summarize>','</Summarize>','<connectionStrings>','</connectionStrings>','<|reserved_special_token_94|>','<$>','<translation>','<DateTime>','<_output>','<product>','</Up trading>','<Key Point>','</Key Point>',}

s_invalid_input_content = {"I'm sorry"}

class XpoDataCheck:
    def __init__(self):
        self.kw_prompt_q = 'Question'
        self.kw_think = 'think'
        self.kw_answer = 'answer'
        self.max_length = 8192
        self.japanese_pattern = re.compile(r'[\u3040-\u30ff\u31f0-\u31ff]+')
        self.zh_pattern = re.compile('[\u4e00-\u9fa5]')
        self.korean_pattern = re.compile(r'[\uac00-\ud7a3]')
        self.arabic_pattern = re.compile(r'[\u0600-\u06FF]')
        self.target_template = '<think>\n{thought}\n</think>\n<answer>\n{answer}\n</answer>'

    @staticmethod
    def extract(sen, item, item_end=None):
        try:
            if '<' not in item and '>' not in item:
                _ = sen[re.search(f'<{item}>', sen).end():re.search(f'</{item}>', sen).start()].strip()
            else:
                _ = sen[re.search(f'{item}', sen).end():re.search(f'{item_end}', sen).start()].strip()
        except:
            _ = ''
        return _

    def language_filter(self, data, only_chosen=True):
        if (self.japanese_pattern.search(str(data)) or
                self.korean_pattern.search(str(data)) or self.arabic_pattern.search(str(data))):
            return False, 'Wrong language character'
        # q-language: en/zh
        chosen_input=data['chosen'][-2]['content']
        chosen_target = data['chosen'][-1]['content']
        rejected_input = data['rejected'][-2]['content']
        rejected_target = data['rejected'][-1]['content']
        if self.zh_pattern.search(chosen_input):  # q-zh -> a-zh ratio>=0.7
            if len(re.sub('[\u4e00-\u9fa5\d]+', '', chosen_target)) / len(chosen_target) > 0.3:
                return False, 'QA language mismatch in chosen'
        else:
            if self.zh_pattern.search(chosen_target):  # q-en -> a-en
                return False, 'QA language mismatch in chosen'
        if not only_chosen:
            if self.zh_pattern.search(rejected_input):  # q-zh -> a-zh ratio>=0.7
                if len(re.sub('[\u4e00-\u9fa5\d]+', '', rejected_target)) / len(rejected_target) > 0.3:
                    return False, 'QA language mismatch in target'
            else:
                if self.zh_pattern.search(rejected_target):  # q-en -> a-en
                    return False, 'QA language mismatch in target'
        return True, 'Language check passed'

    def basic_check(self, data):
        # input
        if data['chosen'][-2]['content'] != data['rejected'][-2]['content']:
            return False, 'Chosen & rejected input mismatch'
        # # 模板校验
        # _q = self.extract(data['chosen'][-2]['content'], self.kw_prompt_q)
        # if prompt_template.format(question=_q) != data['chosen'][-2]['content']:
        #     return False, 'input is not consistent with prompt template'

        # target
        chosen_content = data['chosen'][-1]['content']
        rejected_content = data['rejected'][-1]['content']
        if chosen_content == rejected_content:
            return False, 'Chosen & rejected target is same!'

        chosen_think = self.extract(chosen_content, self.kw_think).strip()
        rejected_think = self.extract(rejected_content, self.kw_think).strip()
        chosen_answer = self.extract(chosen_content, self.kw_answer).strip()
        rejected_answer = self.extract(rejected_content, self.kw_answer).strip()

        if len(chosen_think) < 200:
            return False, 'Length of chosen answer think part less than 200 characters.'
        if len(rejected_think) < 200:
            return False, 'Length of rejected answer think part less than 200 characters.'
        if len(chosen_answer) == 0:
            return False, 'No answer from chosen answer'
        if len(rejected_answer) == 0:
            return False, 'No answer from rejected answer'
        if chosen_answer == rejected_answer:
            return False, 'Chosen answer is the same as rejected answer'
        return True, 'basic check passed'

    @staticmethod
    def show(data):
        print(data['chosen'][-2]['content'])
        print('=' * 100)
        print(data['chosen'][-1]['content'])
        print('=' * 100)
        print(data['rejected'][-1]['content'])

    def process(self, data):
        flag, msg = self.basic_check(data)
        if not flag:
            return None, flag, msg
        flag, msg = self.language_filter(data)
        if not flag:
            return None, flag, msg
        if 'Sure, here' in data['chosen'][-2]['content'] or any(
                [_ in data['chosen'][-1]['content'] for _ in s_invalid_input_content]):
            return None, False, 'invalid term appeared in input/target'
        # chosen & rejected 部分都需要过滤，否则rejected 部分太离谱容易造成hacking
        # chosen
        thought_chosen = self.extract(data['chosen'][1]['content'], 'think')
        ans_chosen = self.extract(data['chosen'][1]['content'], 'answer')
        # rejected
        thought_rejected = self.extract(data['rejected'][1]['content'], 'think')
        ans_rejected = self.extract(data['rejected'][1]['content'], 'answer')
        for _ in s_invalid_special_tokens:
            if _ in thought_chosen + thought_rejected:
                return None, False, f'Invalid special token: {_} appeared in data!'
        if len(thought_chosen) > 200 and len(thought_rejected) > 200:
            if len(str(data['chosen'])) > self.max_length or len(str(data['rejected'])) > self.max_length:
                return None, False, f'data length is larger than {self.max_length}'
            _fixed = {**data}
        else:
            return None, False, 'Length of chosen/rejected answer think part less than 200 characters.'
        # 抽q 插template
        _fixed['chosen'][0]['content'] = prompt_template.format(
            question=self.extract(_fixed['chosen'][0]['content'], self.kw_prompt_q))
        _fixed['rejected'][0]['content'] = _fixed['chosen'][0]['content']
        # ans
        _fixed['chosen'][1][
            'content'] = self.target_template.format(thought=thought_chosen.strip(), answer=ans_chosen.strip())
        _fixed['rejected'][1][
            'content'] = self.target_template.format(thought=thought_rejected.strip(), answer=ans_rejected.strip())

        return _fixed, True, 'main check passed!'
