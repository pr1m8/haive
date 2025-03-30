# Main graph
def initiate_all_interviews(state: ResearchGraphState):
    """ This is the "map" step where we run each interview sub-graph using Send API """

    topic = state["topic"]
    return [Send("Create podcast", {"topic": topic,
                                        "messages": [HumanMessage(
                                            content=f"So you said you were researching about {subtopic}?"
                                        )
                                                    ]}) for subtopic in state["subtopics"]]

def write_report(state: ResearchGraphState):
    # Full set of sections
    sections = state["sections"]
    topic = state["topic"]

    # Concat all sections together
    formatted_str_sections = "\n\n".join([f"{section}" for section in sections])

    # Summarize the sections into a final report
    system_message = report_writer_instructions.format(topic=topic, context=formatted_str_sections)
    report = podcast_model.send_message(system_message)
    return {"content": report.text}

def write_introduction(state: ResearchGraphState):
    # Full set of sections
    sections = state["sections"]
    topic = state["topic"]

    # Concat all sections together
    formatted_str_sections = "\n\n".join([f"{section}" for section in sections])

    # Summarize the sections into a final report

    instructions = intro_instructions.format(topic=topic, formatted_str_sections=formatted_str_sections)
    intro = podcast_model.send_message(instructions)
    return {"introduction": intro.text}

def write_conclusion(state: ResearchGraphState):
    # Full set of sections
    sections = state["sections"]
    topic = state["topic"]

    # Concat all sections together
    formatted_str_sections = "\n\n".join([f"{section}" for section in sections])

    # Summarize the sections into a final report

    instructions = conclusion_instructions.format(topic=topic, formatted_str_sections=formatted_str_sections)
    conclusion = podcast_model.send_message(instructions)
    return {"conclusion": conclusion.text}

def finalize_report(state: ResearchGraphState):
    """ The is the "reduce" step where we gather all the sections, combine them, and reflect on them to write the intro/conclusion """
    # Save full final report
    content = state["content"]
    final_report = state["introduction"] + "\n\n---\n\n" + content + "\n\n---\n\n" + state["conclusion"]

    return {"final_report": final_report}

def Start_parallel(state):
    """ No-op node that should be interrupted on """
    pass