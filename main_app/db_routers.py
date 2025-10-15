class RailwayRouter:
    """
    A router to control all database operations on models in specific apps.
    Use 'railway' database for specific apps or as a backup.
    """

    # Example: route models in 'analytics' app to Railway
    route_app_labels = {'analytics', 'backup'}

    def db_for_read(self, model, **hints):
        """Point read operations."""
        if model._meta.app_label in self.route_app_labels:
            return 'railway'
        return None  # Use default

    def db_for_write(self, model, **hints):
        """Point write operations."""
        if model._meta.app_label in self.route_app_labels:
            return 'railway'
        return None  # Use default

    def allow_relation(self, obj1, obj2, **hints):
        """Allow relations if both objects are in same DB."""
        db_list = ('default', 'railway')
        if obj1._state.db in db_list and obj2._state.db in db_list:
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """Control which DB migrations apply to."""
        if app_label in self.route_app_labels:
            return db == 'railway'
        return db == 'default'
