from conan import ConanFile

from conan.tools.files import copy # uncomment only if you need the copy function of conan2

class MyConanFile(ConanFile):
    name = "my_conan_file"
    version = "1.0.0"

    # this is just for demo purpose options and default options should be injected
    # from conandata.yml file
    options = {
        "option_a": [True, False],
        "option_b": ["var1", "var2", "var3"]
    }

    default_options = {
        "option_a": True,
        "option_b": "var1"
    }

    exclude_list = [
        ".git/*",
        ".gitignore",
        ".gitmodules",
        ".gitattributes",
        "conan*",
        "dependency_info.json",
        "graph_info.json",
        "quality_container/*"
    ]

    def init(self):
        if local_options := self.conan_data.get("local_options", None):
            self.output.info("add options from conandata.yml file")
            for option_name in local_options:
                self.output.info(f"my option {option_name}: {local_options[option_name]}")
                # inject my options here

    def package(self):
        # copy source files
        copy_pattern = []
        if package_content := self.conan_data.get("package_content", None):
            if default_content := package_content.get("default", None):
                for pattern in default_content:
                    copy_pattern.append(pattern)

            for option_key, _ in self.options.items():
                self.output.info(f"1. Processing {option_key}")
                if option_value := self.options.get_safe(option_key):
                    self.output.info(f"2. Processing {option_key} with value {option_value}")
                    if conandata_options := package_content.get(option_key, None):
                        self.output.info(f"3. Processing {conandata_options}")
                        if hasattr(conandata_options, "items"):
                            for conandata_option_key, conandata_option_value in conandata_options.items():
                                self.output.info(f"4. Processing {conandata_option_value} of {conandata_option_key}")
                                if conandata_option_key == option_value:
                                    self.output.info(f"5. Processing {conandata_option_value} of {conandata_option_key}")
                                    for file_pattern in conandata_option_value:
                                        self.output.info(f"6. Processing {file_pattern}")
                                        copy_pattern.append(file_pattern)
                        else:
                            for file_pattern in conandata_options:
                                copy_pattern.append(file_pattern)



        self.output.info(f"copy pattern: {copy_pattern}")
        for pattern in copy_pattern:
            copy(self, pattern, self.source_folder, self.package_folder, keep_path=True, excludes=self.exclude_list)
