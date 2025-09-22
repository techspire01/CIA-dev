// JavaScript for dynamic category field in Supplier admin
(function($) {
    $(document).ready(function() {
        var categoryField = $('#id_category');
        var newCategoryField = $('#id_new_category').closest('.form-row, .form-group');
        if (!newCategoryField.length) {
            newCategoryField = $('#id_new_category').parent();
        }
        function toggleNewCategory() {
            if (categoryField.val() === '__add_new__') {
                newCategoryField.show();
            } else {
                newCategoryField.hide();
            }
        }
        toggleNewCategory();
        categoryField.change(toggleNewCategory);
    });
})(django.jQuery);
