import re

class SemanticAnalyzer:
    def __init__(self, code_lines):
        self.lines = code_lines.split('\n')
        self.errors = []
        self.properties = {}  # nome -> set de tipos ('data' e/ou 'object')

    def analyze(self):
        self.errors.clear()
        self.properties.clear()

        self.check_header_order()
        self.check_closure_order()
        self.check_type_coercion()
        self.check_property_overloading()
        self.check_invalid_operators()
        self.check_first_section_after_class()

        self.errors.sort(key=self.extract_line_number)
        return self.classify_properties(), self.errors

    def classify_properties(self):
        """
        Gera lista formatada de propriedades que têm apenas um tipo definido
        ('Data Property' ou 'Object Property').
        """
        classified = []
        for prop, tipos in sorted(self.properties.items()):
            if len(tipos) == 1:
                tipo_str = "Data Property" if 'data' in tipos else "Object Property"
                classified.append(f"{prop}: {tipo_str}")
        return classified

    def extract_line_number(self, msg):
        match = re.match(r"Linha (\d+):", msg)
        return int(match.group(1)) if match else 0

    def check_header_order(self):
        expected_order = ['Class:', 'EquivalentTo:', 'SubClassOf:', 'DisjointClasses:', 'Individuals:']
        current_headers = []
        current_class = None
        header_lines = {}

        for lineno, line in enumerate(self.lines, 1):
            for keyword in expected_order:
                if line.strip().startswith(keyword):
                    current_headers.append(keyword)
                    header_lines[keyword] = lineno

                    if keyword == 'Class:':
                        current_class = line.strip().replace('Class:', '').strip()

        indices = [expected_order.index(h) for h in current_headers]
        if indices != sorted(indices):
            first_line = header_lines[current_headers[0]]
            self.errors.append(f"Linha {first_line}: Ordem inválida de cabeçalhos na classe \"{current_class}\".")

        if 'Individuals:' in current_headers and 'DisjointClasses:' not in current_headers:
            line_indiv = header_lines['Individuals:']
            self.errors.append(f"Linha {line_indiv}: A seção 'Individuals' não pode aparecer antes de 'DisjointClasses:'.")

    def check_first_section_after_class(self):
        current_class = None
        found_first_section = False

        for lineno, line in enumerate(self.lines, 1):
            stripped = line.strip()
            if stripped.startswith("Class:"):
                current_class = stripped.replace("Class:", "").strip()
                found_first_section = False
                continue
            if current_class and not found_first_section and stripped:
                if not (stripped.startswith("SubClassOf:") or stripped.startswith("EquivalentTo:")):
                    self.errors.append(f"Linha {lineno}: A classe \"{current_class}\" não pode iniciar com \"{stripped.split(':')[0]}\".")
                found_first_section = True

    def check_closure_order(self):
        class_blocks = self.split_by_class()
        for class_name, block in class_blocks.items():
            seen_some = set()
            for line in block:
                lineno = self.find_line_number(line)
                if ' some ' in line:
                    prop = self.extract_property(line)
                    if prop:
                        seen_some.add(prop)
                if ' only ' in line:
                    prop = self.extract_property(line)
                    if prop and prop not in seen_some:
                        self.errors.append(f"Linha {lineno}: O \"only\" não pode aparecer antes de \"some\" na classe \"{class_name}\".")

    def check_type_coercion(self):
        pattern = r'\[ *(>=|<=|<|>|==)? *(-?\d+) *\]'
        for lineno, line in enumerate(self.lines, 1):
            if re.search(pattern, line):
                if not any(dtype in line for dtype in ['xsd:', 'owl:', 'rdf:', 'rdfs:']):
                    self.errors.append(f"Linha {lineno}: Valor com operador relacional sem tipo de dado explícito.")

    def check_invalid_operators(self):
        invalid_ops = ['<<', '>>', '><', '<>', '==>', '===']
        for lineno, line in enumerate(self.lines, 1):
            for op in invalid_ops:
                if op in line:
                    self.errors.append(f"Linha {lineno}: Operador inválido '{op}'.")

    def check_property_overloading(self):
        prop_types = {}

        for lineno, line in enumerate(self.lines, 1):
            match = re.match(r'\s*(\w+)\s+(some|min|max|exactly)\s+(.+)', line)
            if match:
                prop, quant, target = match.groups()
                target = target.strip()

                if target.startswith(('xsd:', 'owl:', 'rdf:', 'rdfs:')):
                    tipo = 'data'
                elif re.match(r'^[A-Z][a-zA-Z0-9_]*$', target):
                    tipo = 'object'
                else:
                    tipo = None

                if tipo:
                    if prop not in prop_types:
                        prop_types[prop] = set()
                    prop_types[prop].add(tipo)
                else:
                    self.errors.append(f"Linha {lineno}: Tipo indefinido ou inválido da propriedade '{prop}'.")

        # Salva propriedades com tipos únicos
        self.properties = prop_types

        for prop, tipos in prop_types.items():
            if 'data' in tipos and 'object' in tipos:
                linha_prop = next(
                    (i+1 for i, line in enumerate(self.lines) if line.strip().startswith(prop + ' ')),
                    '?'
                )
                self.errors.append(f"Linha {linha_prop}: Propriedade '{prop}' está sobrecarregada como data property e object property.")

    def split_by_class(self):
        class_blocks = {}
        current_class = None
        current_lines = []

        for line in self.lines:
            if line.strip().startswith("Class:"):
                if current_class:
                    class_blocks[current_class] = current_lines
                current_class = line.strip().replace("Class:", "").strip()
                current_lines = []
            elif current_class:
                current_lines.append(line)
        if current_class:
            class_blocks[current_class] = current_lines

        return class_blocks

    def extract_property(self, line):
        match = re.match(r'\s*(\w+)\s+(some|only|min|max|exactly)', line)
        return match.group(1) if match else None

    def find_line_number(self, line_content):
        for idx, content in enumerate(self.lines, 1):
            if line_content.strip() == content.strip():
                return idx
        return "?"
