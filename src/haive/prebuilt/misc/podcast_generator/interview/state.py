class InterviewState(MessagesState):
    topic: str # Topic of the podcast
    max_num_turns: int # Number turns of conversation
    context: Annotated[list, operator.add] # Source docs
    section: str # section transcript
    sections: list # Final key we duplicate in outer state for Send() API