from app import App

class GenShopifyExcel(App):
    FIELDNAMES = [
        "Handle",
        "Title",
        "Body (HTML)",
        "Vendor",
        "Product",
        "Category",
        "Type",
        "Tags",
        "Published",
        "Option1 Name",
        "Option1 Value",
        "Option2 Name",
        "Option2 Value",
        "Option3 Name",
        "Option3 Value",
        "Variant SKU",
        "Variant Grams",
        "Variant Inventory Tracker",
        "Variant Inventory Qty",
        "Variant Inventory Policy",
        "Variant Fulfillment Service",
        "Variant Price",
        "Variant Compare At Price",
        "Variant Requires Shipping",
        "Variant Taxable",
        "Variant Barcode",
        "Image Src",
        "Image Position",
        "Image Alt Text",
        "Gift Card",
        "SEO Title",
        "SEO Description",
        "Google Shopping / Google Product Category",
        "Google Shopping / Gender",
        "Google Shopping / Age Group",
        "Google Shopping / MPN",
        "Google Shopping / AdWords Grouping",
        "Google Shopping / AdWords Labels",
        "Google Shopping / Condition",
        "Google Shopping / Custom Product",
        "Google Shopping / Custom Label 0",
        "Google Shopping / Custom Label 1",
        "Google Shopping / Custom Label 2",
        "Google Shopping / Custom Label 3",
        "Google Shopping / Custom Label 4",
        "Variant Image",
        "Variant Weight Unit",
        "Variant Tax Code",
        "Cost per item",
        "Price / International",
        "Compare At Price / International",
        "Status",
    ]

    def fill_with_data(self, data, is_parent: bool, idx, a1v=None, a2v=None):
        return {
            "Handle": data['Handle'],
            "Title": data['Name'] if is_parent else "",
            "Body (HTML)": data['Description'] if is_parent else "",
            "Vendor": data['Vendor'] if is_parent else "",
            "Product Category": "",
            "Type": data['Type'] if is_parent else "",
            "Tags": data['Tags'] if is_parent else "",
            "Published": "TRUE" if is_parent else "",
            "Option1 Name": data['Attribute 1 name'] if is_parent else "",
            "Option1 Value": "" if a1v is None or (is_parent and len(data['Attribute 1 value(s)']) > 0) else a1v.strip(),
            "Option2 Name": data['Attribute 2 name'] if is_parent else "",
            "Option2 Value": "" if a2v is None or (is_parent and len(data['Attribute 2 value(s)']) > 0) else a2v.strip(),
            "Option3 Name": "",
            "Option3 Value": "",
            "Variant SKU": data['SKU'] if is_parent else data['SKU'] + "-" + str(idx),
            "Variant Grams": "0",
            "Variant Inventory Tracker": "shopify",
            "Variant Inventory Qty": data['Stock'],
            "Variant Inventory Policy": "continue",
            "Variant Fulfillment Service": "manual",
            "Variant Price": data['Sale price'],
            "Variant Compare At Price": data['Regular price'],
            "Variant Requires Shipping": "TRUE",
            "Variant Taxable": "FALSE",
            "Variant Barcode": "",
            "Image Src": data['Images'] if is_parent else "",
            "Image Position": str(idx),
            "Image Alt Text": "",
            "Gift Card": "FALSE" if is_parent else "",
            "SEO Title": "",
            "SEO Description": "",
            "Google Shopping / Google Product Category": "",
            "Google Shopping / Gender": "",
            "Google Shopping / Age Group": "",
            "Google Shopping / MPN": "",
            "Google Shopping / AdWords Grouping": "",
            "Google Shopping / AdWords Labels": "",
            "Google Shopping / Condition": "",
            "Google Shopping / Custom Product": "",
            "Google Shopping / Custom Label 0": "",
            "Google Shopping / Custom Label 1": "",
            "Google Shopping / Custom Label 2": "",
            "Google Shopping / Custom Label 3": "",
            "Google Shopping / Custom Label 4": "",
            "Variant Image": "",
            "Variant Weight Unit": "kg",
            "Variant Tax Code": "",
            "Cost per item": "",
            "Price / International": "",
            "Compare At Price / International": "",
            "Status": "active" if is_parent else "",
        }

    def process(self):
        # input filename
        input_filename = self.input("请将待处理的csv文件拖动到此窗口内：")
        output_filename = self.addSuffixToFilename(input_filename, '-shopify-upload')

        # read from input file
        input_data = self.readCsvToDict(input_filename)

        output_data = list()
        for line in input_data:
            self.printCounter(line['SKU'])
            sub_idx = 0
            is_parent = True
            # generate output data of parent item
            output_data.append(
                self.fill_with_data(line, is_parent, sub_idx)
            )

            # process sub items
            is_parent = False
            for a1v in line['Attribute 1 value(s)'].split(','):
                for a2v in line['Attribute 2 value(s)'].split(','):
                    sub_idx += 1
                    output_data.append(
                        self.fill_with_data(line, is_parent, sub_idx, a1v, a2v)
                    )

        # write to output file
        self.writeCsvFromDict(output_filename, output_data)


if __name__ == "__main__":
    app = GenShopifyExcel()
    app.run()