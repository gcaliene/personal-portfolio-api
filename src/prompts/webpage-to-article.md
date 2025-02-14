# Webpage to Article Schema Template

## 1. Extract Content
- Title → content.title
- Summary → content.summary 
- Author, date, category/tags
- Main content sections

## 2. JSON Structure
```json
{
    "url": "webpage-url",
    "version": 1,
    "type": "blog",
    "content": {
        "title": "Extracted Title",
        "summary": "Brief Overview",
        "main_content": "<article class=\"max-w-4xl mx-auto\">...</article>",
        "author": "Author Name",
        "publish_date": "YYYY-MM-DD"
    },
    "category": "main-category",
    "subcategory": "sub-category",
    "tags": ["tag1", "tag2"],
    "status": "published",
    "created_by": "author-id",
    "updated_by": "author-id",
    "deleted_at": null,
    "deleted_by": null
}
```

## 3. HTML Templates

### Section Template:
```html
<section id="section-id">
    <h2 class="text-3xl font-bold mb-4 mt-8">Section Title</h2>
    <p class="text-lg text-gray-700 dark:text-gray-300 mb-6">Content...</p>
</section>
```

### Code Block Template:
```html
<div class="code-block" style="background:#f6f8fa; padding:16px; border-radius:6px; margin:16px 0; overflow-x:auto;">
    <h4 style="margin-top:0; color:#57606a;">Example:</h4>
    <pre style="margin:0"><code class="language-[lang]">
        // Code here
    </code></pre>
</div>
```

## 4. Requirements
JSON:
- Use consistent indentation
- Include all required fields
- Proper value formatting (dates: YYYY-MM-DD)
- Null values where appropriate

HTML:
- Escape HTML in main_content 
- Use &lt; and &gt; for code examples
- Remove DOCTYPE/html/head/body tags
- Wrap in article tag with max-w-4xl mx-auto class

Article Structure:
1. Introduction
2. Topic sections with headings
3. Code examples where relevant
4. Conclusion paragraph