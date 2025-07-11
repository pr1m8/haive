class InstructionComponent(BaseModel):
    """Individual instruction component with metadata."""

    component_id: UUID = Field(default_factory=uuid4)
    instruction_text: str = Field(..., min_length=10, max_length=2000)
    priority: int = Field(default=1, ge=1, le=10)
    effectiveness_score: float = Field(default=0.5, ge=0.0, le=1.0)
    usage_count: int = Field(default=0, ge=0)
    last_modified: datetime = Field(default_factory=datetime.now)

    @field_validator("instruction_text")
    @classmethod
    def validate_instruction_clarity(cls, v: str) -> str:
        """Validate instruction clarity and format."""
        v = v.strip()
        if not v.endswith(".") and not v.endswith("!") and not v.endswith("?"):
            v += "."

        # Check for imperative mood (simplified)
        imperative_starters = [
            "use",
            "avoid",
            "ensure",
            "always",
            "never",
            "when",
            "if",
        ]
        if not any(v.lower().startswith(starter) for starter in imperative_starters):
            # This is a simplified check; real implementation might use NLP
            pass

        return v


class ReflectionCycle(BaseModel):
    """Reflection cycle for continuous improvement."""

    cycle_id: UUID = Field(default_factory=uuid4)
    trigger_event: str = Field(..., description="What triggered this reflection")
    current_performance: Dict[str, float] = Field(default_factory=dict)
    identified_issues: List[str] = Field(default_factory=list)
    proposed_changes: List[str] = Field(default_factory=list)
    change_rationale: str = Field(..., description="Why these changes are needed")
    confidence_score: float = Field(default=0.5, ge=0.0, le=1.0)

    @model_validator(mode="after")
    def validate_reflection_logic(self) -> "ReflectionCycle":
        """Validate reflection cycle logic."""
        if len(self.proposed_changes) > 10:
            raise ValueError("Too many proposed changes in one cycle (max 10)")

        if self.confidence_score > 0.8 and len(self.identified_issues) == 0:
            raise ValueError("High confidence requires identified issues")

        return self


class ProceduralMemory(BaseMemoryModel, TemporalMixin):
    """Advanced procedural memory with self-modification capabilities."""

    __memory_type__ = "procedural"
    __validation_level__ = "enterprise"

    agent_id: str = Field(..., description="Agent identifier")
    instruction_set_name: str = Field(..., description="Instruction set identifier")

    # Core instructions
    core_instructions: List[InstructionComponent] = Field(default_factory=list)
    contextual_modifiers: Dict[str, List[str]] = Field(default_factory=dict)

    # Performance tracking
    overall_effectiveness: float = Field(default=0.5, ge=0.0, le=1.0)
    usage_statistics: Dict[str, int] = Field(default_factory=dict)
    performance_trends: List[Dict[str, Any]] = Field(default_factory=list)

    # Reflection and adaptation
    reflection_cycles: List[ReflectionCycle] = Field(default_factory=list)
    last_reflection: Optional[datetime] = Field(None)
    adaptation_threshold: float = Field(default=0.3, ge=0.0, le=1.0)

    # Version control
    version: int = Field(default=1, ge=1)
    change_log: List[Dict[str, Any]] = Field(default_factory=list)

    @field_validator("core_instructions")
    @classmethod
    def validate_instruction_set(
        cls, v: List[InstructionComponent]
    ) -> List[InstructionComponent]:
        """Validate instruction set consistency."""
        if len(v) == 0:
            raise ValueError("At least one core instruction required")

        if len(v) > 50:
            raise ValueError("Too many core instructions (max 50)")

        # Check for conflicting instructions (simplified)
        texts = [instr.instruction_text.lower() for instr in v]
        for i, text1 in enumerate(texts):
            for _j, text2 in enumerate(texts[i + 1 :], i + 1):
                if "never" in text1 and "always" in text2:
                    # Simplified conflict detection
                    words1 = set(text1.split())
                    words2 = set(text2.split())
                    if len(words1 & words2) > 3:  # Some overlap
                        # Could indicate conflict, but simplified check
                        pass

        return v

    @model_validator(mode="after")
    def validate_procedural_integrity(self) -> "ProceduralMemory":
        """Validate overall procedural memory integrity."""
        # Update overall effectiveness based on components
        if self.core_instructions:
            total_effectiveness = sum(
                instr.effectiveness_score for instr in self.core_instructions
            )
            self.overall_effectiveness = total_effectiveness / len(
                self.core_instructions
            )

        # Check if reflection is needed
        if self.should_trigger_reflection():
            self._add_reflection_trigger("Performance threshold reached")

        return self

    def should_trigger_reflection(self) -> bool:
        """Determine if reflection cycle should be triggered."""
        if self.overall_effectiveness < self.adaptation_threshold:
            return True

        if self.last_reflection is None:
            return True

        days_since_reflection = (datetime.now() - self.last_reflection).days
        return days_since_reflection > 30  # Monthly reflection

    def _add_reflection_trigger(self, trigger: str) -> None:
        """Add a reflection trigger event."""
        # This would be called by the agent's reflection process

    def generate_instruction_text(self) -> str:
        """Generate formatted instruction text for agent use."""
        sections = []

        # Sort instructions by priority
        sorted_instructions = sorted(
            self.core_instructions, key=lambda x: (-x.priority, -x.effectiveness_score)
        )

        sections.append("=== CORE INSTRUCTIONS ===")
        for instr in sorted_instructions:
            sections.append(f"• {instr.instruction_text}")

        # Add contextual modifiers
        if self.contextual_modifiers:
            sections.append("\n=== CONTEXTUAL GUIDELINES ===")
            for context, modifiers in self.contextual_modifiers.items():
                sections.append(f"When {context}:")
                for modifier in modifiers:
                    sections.append(f"  - {modifier}")

        return "\n".join(sections)

    def adapt_from_reflection(self, reflection: ReflectionCycle) -> None:
        """Adapt instructions based on reflection cycle."""
        if reflection.confidence_score < 0.6:
            return  # Don't adapt on low confidence

        # Apply proposed changes (simplified implementation)
        for change in reflection.proposed_changes:
            if "add instruction" in change.lower():
                # Extract and add new instruction
                new_text = change.split(":")[-1].strip() if ":" in change else change
                new_instruction = InstructionComponent(instruction_text=new_text)
                self.core_instructions.append(new_instruction)

        # Update version and change log
        self.version += 1
        self.change_log.append(
            {
                "version": self.version,
                "timestamp": datetime.now().isoformat(),
                "reflection_id": str(reflection.cycle_id),
                "changes": reflection.proposed_changes,
            }
        )

        self.last_reflection = datetime.now()
        self.reflection_cycles.append(reflection)
