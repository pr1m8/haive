{{ name | title }} Command
{{ "=" * (name|length + 8) }}

.. currentmodule:: {{ module }}

.. card:: 🖥️ Command: ``{{ name }}``
   :class-card: sd-rounded-3 sd-shadow-sm
   :class-header: sd-bg-dark sd-text-white

   **CLI Command**: {{ name }}

   {% if is_click_command %}
   .. click:: {{ module }}:{{ func_name }}
      :prog: {{ prog_name }}
      :nested: full
   {% elif is_argparse_command %}
   .. argparse::
      :module: {{ module }}
      :func: {{ func_name }}
      :prog: {{ prog_name }}
   {% endif %}

.. tab-set::

   .. tab-item:: Usage Examples
      :sync: usage

      .. prompt:: bash $ auto

         # Basic usage
         $ {{ prog_name }} {{ name }} --help
         
         # Common example
         $ {{ prog_name }} {{ name }} [OPTIONS]

      {% if examples %}
      **Real Examples:**

      {% for example in examples %}
      .. prompt:: bash $ auto

         {{ example.command }}
         {{ example.output if example.output }}
      {% endfor %}
      {% endif %}

   .. tab-item:: Live Test
      :sync: test

      .. exec_code::
         :caption: Test command availability
         :linenos:

         import subprocess
         import sys

         # Test if command is available
         try:
             result = subprocess.run(['{{ prog_name }}', '{{ name }}', '--help'], 
                                   capture_output=True, text=True, timeout=5)
             if result.returncode == 0:
                 print("✅ Command available")
                 print(f"📝 Help preview: {result.stdout.split()[0:10]}")
             else:
                 print("ℹ️ Command structure available")
         except Exception as e:
             print(f"ℹ️ Command info: {e}")

   .. tab-item:: Parameters
      :sync: params

      .. admonition:: 💡 Parameter Tips
         :class: tip

         * Use :tippy:`--help <Always check help for latest options>` to see all available options
         * Parameters with :paramlink:`type hints <Click parameter names for details>` show expected formats
         * Use :emoji:`books` environment variables when supported

.. dropdown:: 🔍 Live Command Output
   :color: info
   :icon: terminal

   .. autorun:: python3

      import subprocess
      import sys
      
      print(f"🖥️ Testing command: {{ prog_name }} {{ name }}")
      
      # Test help output
      try:
          result = subprocess.run(
              ['{{ prog_name }}', '{{ name }}', '--help'],
              capture_output=True, text=True, timeout=10
          )
          if result.returncode == 0:
              print("✅ Command available")
              lines = result.stdout.split('\n')[:10]
              print("\n📝 Help preview:")
              for line in lines:
                  if line.strip():
                      print(f"  {line}")
          else:
              print("ℹ️ Command structure documented")
      except Exception as e:
          print(f"🔧 Command info available: {e}")
      
      # Show version if available
      try:
          version_result = subprocess.run(
              ['{{ prog_name }}', '{{ name }}', '--version'],
              capture_output=True, text=True, timeout=5
          )
          if version_result.returncode == 0:
              print(f"🏷️ Version: {version_result.stdout.strip()}")
      except:
          pass

.. admonition:: 🚀 Quick Reference
   :class: note

   **Command**: ``{{ prog_name }} {{ name }}``
   
   **Purpose**: {{ description if description else 'Command line interface' }}
   
   **Module**: ``{{ module }}``
   
   .. last-updated:: {{ name }}
      :format: Last updated: %Y-%m-%d %H:%M
      
   .. versionadded:: 1.0
      Command line interface for {{ name }}

.. grid:: 1 2 2 2
   :gutter: 2

   .. grid-item-card:: 📄 Documentation
      :shadow: sm
      
      * :doc:`/cli/index` - All commands
      * :doc:`/examples/cli` - Usage examples
      * :issue:`123` - Feature requests

   .. grid-item-card:: 🔗 Related
      :shadow: sm
      
      * :doc:`/api/{{ module.replace('.', '/') }}` - API docs
      * :pr:`456` - Recent improvements
      * :commit:`abc123` - Latest changes

.. seealso::

   * :doc:`/cli/index` - All CLI commands
   * :doc:`/examples/cli` - CLI usage examples
   * :doc:`/api/{{ module.replace('.', '/') }}` - API documentation