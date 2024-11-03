from settings import *
from functools import lru_cache

class Cache:
    def __init__(self):
        self.stacked_sprite_cache = {}
        self.entity_sprite_cache = {}
        self.viewing_angle = 360 // NUM_ANGLES
        self.outline_thickness = 5
        self.alpha_value = 70
        self.get_stacked_sprite_cache()
        self.get_entity_sprite_cache()

    def get_entity_sprite_cache(self):
        for sprite_name in ENTITY_SPRITE_ATTRS:
            self.entity_sprite_cache[sprite_name] = {
                'images': None
            }
            attrs = ENTITY_SPRITE_ATTRS[sprite_name]
            images = self.get_layer_array(attrs)
            self.entity_sprite_cache[sprite_name]['images'] = images

            mask = self.get_entity_mask(attrs, images)
            self.entity_sprite_cache[sprite_name]['mask'] = mask

    def get_entity_mask(self, attrs, images):
        path = attrs.get('mask_path', False)
        if not path:
            return pg.mask.from_surface(images[0])
        else:
            scale = attrs['scale']
            mask_image = pg.image.load(path).convert_alpha()
            mask_image = pg.transform.scale(mask_image, vec2(mask_image.get_size()) * scale)
            return pg.mask.from_surface(mask_image)

    def get_stacked_sprite_cache(self):
        for obj_name in STACKED_SPRITE_ATTRS:
            self.stacked_sprite_cache[obj_name] = {
                'rotated_sprites': {},
                'alpha_sprites': {},
                'collision_masks': {}
            }
            attrs = STACKED_SPRITE_ATTRS[obj_name]
            layer_array = self.get_layer_array(attrs)
            self.run_prerender(obj_name, layer_array, attrs)

    def run_prerender(self, obj_name, layer_array, attrs):
        outline = attrs.get('outline', True)
        transparency = attrs.get('transparency', False)
        mask_layer = attrs.get('mask_layer', 0)
        num_layers = attrs['num_layers']
        scale = attrs['scale']

        for angle in range(NUM_ANGLES):
            sprite_surf = self.create_sprite_surf(layer_array, angle, attrs)

            # Create collision mask (only once if mask is the same across all angles)
            if angle == 0:  # Generate collision mask for the first angle
                mask = pg.mask.from_surface(sprite_surf)
            self.stacked_sprite_cache[obj_name]['collision_masks'][angle] = mask

            # Add outline if necessary
            if outline:
                self.add_outline(sprite_surf)

            # Add alpha sprites if transparency is enabled
            if transparency:
                alpha_sprite = self.create_alpha_sprite(sprite_surf)
                self.stacked_sprite_cache[obj_name]['alpha_sprites'][angle] = alpha_sprite

            self.stacked_sprite_cache[obj_name]['rotated_sprites'][angle] = sprite_surf

    def create_sprite_surf(self, layer_array, angle, attrs):
        """Create a sprite surface from layer array with the given angle."""
        sprite_surf = pg.Surface([layer_array[0].get_width(), 
                                  layer_array[0].get_height() + attrs['num_layers'] * attrs['scale']])
        sprite_surf.fill('khaki')
        sprite_surf.set_colorkey('khaki')

        # Apply rotations and blit layers
        for ind, layer in enumerate(layer_array):
            rotated_layer = self.get_rotated_sprite(layer, angle)
            sprite_surf.blit(rotated_layer, (0, ind * attrs['scale']))

        return sprite_surf

    def add_outline(self, sprite_surf):
        """Draw an outline around the sprite based on its mask."""
        outline_coords = pg.mask.from_surface(sprite_surf).outline()
        pg.draw.polygon(sprite_surf, 'black', outline_coords, self.outline_thickness)

    def create_alpha_sprite(self, sprite_surf):
        """Create an alpha sprite for transparency."""
        alpha_sprite = sprite_surf.copy()
        alpha_sprite.set_alpha(self.alpha_value)
        return pg.transform.flip(alpha_sprite, True, True)

    @lru_cache(maxsize=None)
    def get_rotated_sprite(self, sprite, angle):
        """Rotate sprite and cache the result for performance."""
        return pg.transform.rotate(sprite, angle * self.viewing_angle)

    def get_layer_array(self, attrs):
        """Extract layers from a sprite sheet based on the given attributes."""
        sprite_sheet = pg.image.load(attrs['path']).convert_alpha()
        sprite_sheet = pg.transform.scale(sprite_sheet, vec2(sprite_sheet.get_size()) * attrs['scale'])

        sheet_width = sprite_sheet.get_width()
        sheet_height = sprite_sheet.get_height()
        sprite_height = sheet_height // attrs['num_layers']
        sheet_height = sprite_height * attrs['num_layers']

        # Get individual layers
        layer_array = []
        for y in range(0, sheet_height, -sprite_height):
            sprite = sprite_sheet.subsurface((0, y, sheet_width, sprite_height))
            layer_array.append(sprite)

        return layer_array[::-1]  # Reverse order of layers
