# Webpage to Article Schema Prompt Template

When given a webpage source, please:

1. First analyze and extract:
   - Main title (for content.title)
   - Brief overview (for content.summary)
   - Main content sections
   - Author
   - date
   - Category and subcategory
   - Relevant tags

2. Format the content into a structured article with:
   - Introduction 
   - Major topic sections with descriptive headings
   - Each section should include:
     * A descriptive heading using Tailwind classes: `text-3xl font-bold mb-4 mt-8 text-gray-900 dark:text-white`
     * Explanatory paragraphs using: `text-lg text-gray-700 dark:text-gray-300 mb-6`
     * Be sure to include relevant code examples in blocks with:
       ```
       class="code-block" style="background: #f6f8fa; padding: 16px; border-radius: 6px; margin: 16px 0; overflow-x: auto;"
       ```
   - A concluding paragraph (without a heading) using the same paragraph styling

3. Structure the output as a JSON object following this schema:
```json
{
    "url": "[appropriate-url]",
    "version": 1,
    "sort_order": 1,
    "type": "blog",
    "content": {
        "title": "[extracted-title]",
        "summary": "[brief-summary]",
        "main_content": "[formatted-html-content]",
        "author": "[author-name]",
        "publish_date": "[date-in-YYYY-MM-DD-format]"
    },
    "category": "[main-category]",
    "subcategory": "[sub-category]",
    "tags": ["relevant", "tags", "here"],
    "status": "published",
    "created_by": "[author-id]",
    "updated_by": "[author-id]",
}
```

4. Important formatting notes:
   - All HTML in main_content should be properly escaped
   - Code examples should use &lt; and &gt; for < and >
   - Remove any DOCTYPE, html, head, or body tags
   - Wrap content in an article tag with class="max-w-4xl mx-auto"
   - Use consistent spacing and indentation in the JSON output

# Example Code Block Format:
```html
<div class="code-block" style="background: #f6f8fa; padding: 16px; border-radius: 6px; margin: 16px 0; overflow-x: auto;">
    <h4 style="margin-top: 0; color: #57606a;">Example Title:</h4>
    <pre style="margin: 0;">
        <code class="language-javascript" style="font-family: monospace; font-size: 14px; line-height: 1.5;">
            // Your code here
        </code>
    </pre>
</div>
```

# Example Section Format:
```html
<section id="section-id">
    <h2 class="text-3xl font-bold mb-4 mt-8 text-gray-900 dark:text-white">Section Title</h2>
    <p class="text-lg text-gray-700 dark:text-gray-300 mb-6">Section content paragraph...</p>
    <!-- Code blocks if needed -->
</section>
```
