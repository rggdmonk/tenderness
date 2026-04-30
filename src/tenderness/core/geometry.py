# Copyright 2026 Pavel Stepachev
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Geometry primitives for cairo/pango rendering."""

from __future__ import annotations

import math
from dataclasses import dataclass, field

import cairo  # noqa: TC002


@dataclass(slots=True, frozen=True)
class BoxSpacing:
    """Spacing values for the four sides of a rectangle.

    Parameters
    ----------
    top
        Top spacing.
    right
        Right spacing.
    bottom
        Bottom spacing.
    left
        Left spacing.
    """

    top: float = 0.0
    right: float = 0.0
    bottom: float = 0.0
    left: float = 0.0

    def horizontal(self) -> float:
        """Total horizontal spacing (left + right)."""
        return self.left + self.right

    def vertical(self) -> float:
        """Total vertical spacing (top + bottom)."""
        return self.top + self.bottom


@dataclass(slots=True, frozen=True)
class Margin(BoxSpacing):
    """Box spacing used as outer margin."""


@dataclass(slots=True, frozen=True)
class Padding(BoxSpacing):
    """Box spacing used as inner padding."""


@dataclass(slots=True, frozen=True)
class Rectangle:
    """An immutable axis-aligned rectangle defined by an origin (x, y) and dimensions, designed for use with cairo/pango (y-down coordinate system).

    Axis-aligned means all sides are parallel to the X and Y axes — no
    rotation is stored. This is also known as an **axis-aligned bounding box**
    (AABB). All spatial operations (``intersects``, ``contains_point``,
    ``distance_to``, etc.) rely on this property and are not valid for rotated
    (oriented) bounding boxes (OBB).

    To work with rotated layouts, transform the rectangle into device space
    first using ``transform(matrix)``, which returns the AABB of the rotated
    shape. The resulting rectangle is always axis-aligned and safe to use with
    all spatial operations.

    Negative width/height are permitted and preserved — the stored origin may
    lie at any corner of the geometric region. All spatial operations use the
    safe ``*_min`` / ``*_max`` bounds, never the raw fields directly.

    Use ``is_non_negative`` to test whether all fields are ``>= 0``.

    Equality is field-level (same origin + dimensions), so two rectangles that
    describe the same region but differ in stored sign will compare unequal::

        Rectangle(0, 0, 10, 10) != Rectangle(10, 10, -10, -10)

    Coordinate system:
        All named corners (``corners``) assume **cairo's y-down convention**:
        y increases downward, so ``y_min`` is visually at the top of the
        rectangle. Do not mix with y-up coordinate systems without flipping
        ``y_min`` / ``y_max``.

    Cairo / Pango safety:
        ``size`` returns the raw stored ``(width, height)``, which may be
        negative. Passing negative dimensions directly to ``ctx.rectangle()``
        or Pango APIs produces silent misbehaviour. Use ``normalized_size``
        when the caller needs guaranteed non-negative values.

    Attributes
    ----------
    x
        X coordinate of the stored origin.
    y
        Y coordinate of the stored origin.
    width
        Stored width; may be negative.
    height
        Stored height; may be negative.
    """

    x: float
    y: float
    width: float
    height: float

    # cached normalized bounds — computed once in __post_init__
    _x_min: float = field(init=False, repr=False, compare=False, hash=False)
    _x_max: float = field(init=False, repr=False, compare=False, hash=False)
    _y_min: float = field(init=False, repr=False, compare=False, hash=False)
    _y_max: float = field(init=False, repr=False, compare=False, hash=False)

    def __post_init__(self) -> None:
        """Compute and cache normalized bounds."""
        x2 = self.x + self.width
        y2 = self.y + self.height
        # object.__setattr__ required because the dataclass is frozen
        object.__setattr__(self, "_x_min", self.x if self.width >= 0 else x2)
        object.__setattr__(self, "_x_max", x2 if self.width >= 0 else self.x)
        object.__setattr__(self, "_y_min", self.y if self.height >= 0 else y2)
        object.__setattr__(self, "_y_max", y2 if self.height >= 0 else self.y)

    # ------------------------------------------------------------------
    # Safe bounds — always x_min <= x_max, y_min <= y_max
    # ------------------------------------------------------------------

    @property
    def x_min(self) -> float:
        """Left edge of the geometric region; always ``<= x_max``."""
        return self._x_min

    @property
    def x_max(self) -> float:
        """Right edge of the geometric region; always ``>= x_min``."""
        return self._x_max

    @property
    def y_min(self) -> float:
        """Upper edge of the geometric region in cairo's y-down system; always ``<= y_max``."""
        return self._y_min

    @property
    def y_max(self) -> float:
        """Lower edge of the geometric region in cairo's y-down system; always ``>= y_min``."""
        return self._y_max

    @property
    def extents(self) -> tuple[float, float, float, float]:
        """``(x_min, y_min, x_max, y_max)`` — safe with negative dimensions."""
        return (self._x_min, self._y_min, self._x_max, self._y_max)

    @property
    def bounds(self) -> tuple[float, float, float, float]:
        """Alias for ``extents`` — industry-standard name."""
        return (self._x_min, self._y_min, self._x_max, self._y_max)

    # ------------------------------------------------------------------
    # Geometry
    # ------------------------------------------------------------------

    @property
    def area(self) -> float:
        """Geometric area; always non-negative."""
        return abs(self.width * self.height)

    @property
    def perimeter(self) -> float:
        """Perimeter of the rectangle; always non-negative."""
        return 2 * (abs(self.width) + abs(self.height))

    @property
    def center(self) -> tuple[float, float]:
        """``(cx, cy)`` of the geometric centre."""
        return ((self._x_min + self._x_max) / 2, (self._y_min + self._y_max) / 2)

    @property
    def size(self) -> tuple[float, float]:
        """``(width, height)`` as stored — may be negative.

        Notes
        -----
        Passing these values directly to ``ctx.rectangle()`` or Pango APIs
        produces silent misbehaviour when either dimension is negative.
        Use ``normalized_size`` when the caller requires non-negative values.
        """
        return (self.width, self.height)

    @property
    def normalized_size(self) -> tuple[float, float]:
        """``(abs(width), abs(height))`` — always non-negative.

        Notes
        -----
        Safe to pass to cairo's ``ctx.rectangle()`` and Pango layout APIs.
        """
        return (abs(self.width), abs(self.height))

    @property
    def aspect_ratio(self) -> float:
        """``abs(width) / abs(height)``.

        Raises
        ------
        ZeroDivisionError
            When ``height`` is exactly ``0``.
        """
        return abs(self.width) / abs(self.height)

    @property
    def diagonal(self) -> float:
        """Euclidean length of the diagonal."""
        return math.hypot(self.width, self.height)

    @property
    def corners(
        self,
    ) -> tuple[
        tuple[float, float],
        tuple[float, float],
        tuple[float, float],
        tuple[float, float],
    ]:
        """``(top-left, top-right, bottom-right, bottom-left)`` using safe bounds.

        Notes
        -----
        "Top" and "bottom" follow **cairo's y-down convention**: ``y_min`` is
        visually above ``y_max`` on screen. Do not interpret these labels in a
        y-up coordinate system.
        """
        x1, y1, x2, y2 = self._x_min, self._y_min, self._x_max, self._y_max
        return ((x1, y1), (x2, y1), (x2, y2), (x1, y2))

    @property
    def is_empty(self) -> bool:
        """``True`` when either dimension is exactly ``0`` (no geometric area).

        Notes
        -----
        Near-zero but non-zero dimensions are not considered empty — that
        judgement belongs to the caller, not the primitive.
        """
        return self.width == 0 or self.height == 0

    @property
    def is_non_negative(self) -> bool:
        """``True`` when all four fields (``x``, ``y``, ``width``, ``height``) are ``>= 0``.

        Notes
        -----
        A passive check — never raises. Use ``validate()`` if you want an
        exception with a per-field message instead.
        """
        return self.x >= 0 and self.y >= 0 and self.width >= 0 and self.height >= 0

    # ------------------------------------------------------------------
    # Spatial relations
    # ------------------------------------------------------------------

    def contains_point(self, px: float, py: float) -> bool:
        """Return ``True`` if the point lies inside or exactly on the boundary.

        Parameters
        ----------
        px
            X coordinate of the point.
        py
            Y coordinate of the point.
        """
        return self._x_min <= px <= self._x_max and self._y_min <= py <= self._y_max

    def contains_rect(self, other: Rectangle) -> bool:
        """Return ``True`` if ``other`` lies entirely within or flush with this rectangle.

        Parameters
        ----------
        other
            The rectangle to test for containment.
        """
        return (
            self._x_min <= other._x_min
            and self._y_min <= other._y_min
            and self._x_max >= other._x_max
            and self._y_max >= other._y_max
        )

    def intersects(self, other: Rectangle) -> bool:
        """Return ``True`` only when the rectangles share a region of positive area.

        Rectangles that merely touch along an edge or at a corner return
        ``False``.

        Parameters
        ----------
        other
            The rectangle to test against.

        See Also
        --------
        touches
        """
        return not (
            self._x_max <= other._x_min
            or other._x_max <= self._x_min
            or self._y_max <= other._y_min
            or other._y_max <= self._y_min
        )

    def touches(self, other: Rectangle) -> bool:
        """Return ``True`` when rectangles share any boundary contact.

        Overlapping or edge/corner adjacent — a superset of ``intersects()``.

        Parameters
        ----------
        other
            The rectangle to test against.

        See Also
        --------
        intersects
        """
        return (
            self._x_max >= other._x_min
            and self._x_min <= other._x_max
            and self._y_max >= other._y_min
            and self._y_min <= other._y_max
        )

    def intersection(self, other: Rectangle) -> Rectangle | None:
        """Return the overlapping region, or ``None`` if they don't intersect.

        Touching-only contact (edge or corner) also returns ``None``, consistent
        with ``intersects()``.

        Parameters
        ----------
        other
            The rectangle to intersect with.
        """
        x1 = max(other._x_min, self._x_min)
        y1 = max(other._y_min, self._y_min)
        x2 = min(other._x_max, self._x_max)
        y2 = min(other._y_max, self._y_max)
        w = x2 - x1
        h = y2 - y1
        return None if w <= 0 or h <= 0 else Rectangle(x=x1, y=y1, width=w, height=h)

    def union(self, other: Rectangle) -> Rectangle:
        """Return the smallest rectangle enclosing both rectangles.

        Parameters
        ----------
        other
            The rectangle to combine with.
        """
        x1 = min(other._x_min, self._x_min)
        y1 = min(other._y_min, self._y_min)
        x2 = max(other._x_max, self._x_max)
        y2 = max(other._y_max, self._y_max)
        return Rectangle(x=x1, y=y1, width=x2 - x1, height=y2 - y1)

    def distance_to(self, other: Rectangle) -> float:
        """
        Shortest distance between the two rectangles.

        Returns `0.0` if they intersect or touch.

        The signed gap along each axis is computed independently, clamped to
        `0` (negative gap means overlap on that axis), then combined with
        `hypot`. This handles all relative positions — left, right, above,
        below, diagonal, overlapping — in a single pass.

        Args:
            other: The rectangle to measure distance to.

        Returns
        -------
            The shortest Euclidean distance, or `0.0` if they touch or overlap.
        """
        dx = max(other._x_min - self._x_max, self._x_min - other._x_max, 0.0)
        dy = max(other._y_min - self._y_max, self._y_min - other._y_max, 0.0)
        return math.hypot(dx, dy)

    def transform(self, matrix: cairo.Matrix) -> Rectangle:
        """Return the axis-aligned bounding box of this rectangle after applying ``matrix``.

        All four corners are transformed through ``matrix`` and the tightest
        enclosing ``Rectangle`` is returned. If ``matrix`` contains rotation,
        the result will be larger than the original — it is the AABB of the
        transformed shape, not the oriented bounding box (OBB) itself.

        Parameters
        ----------
        matrix
            The cairo affine transformation to apply.

        Notes
        -----
        Capture ``matrix`` from ``ctx.get_matrix()`` **inside** the
        ``save/restore`` block, before ``ctx.restore()`` is called —
        otherwise the matrix is already gone.
        """
        transformed = [matrix.transform_point(x, y) for x, y in self.corners]
        xs = [p[0] for p in transformed]
        ys = [p[1] for p in transformed]
        x_min, x_max = min(xs), max(xs)
        y_min, y_max = min(ys), max(ys)
        return Rectangle(x=x_min, y=y_min, width=x_max - x_min, height=y_max - y_min)

    def inset(self, spacing_box: BoxSpacing) -> Rectangle:
        """
        Return the content rectangle after insetting by *spacing_box*.

        Each side moves inward by its corresponding margin value, matching the
        typographic convention: margins define the space between the page edge
        and the content area.  Positive values shrink; negative values expand.

        Args:
            spacing_box: Margin amounts for each side in device units.

        Returns
        -------
            A new ``Rectangle`` with origin ``(x_min + left, y_min + top)``
            and size ``(x_max - x_min - left - right, y_max - y_min - top - bottom)``.
        """
        x = self._x_min + spacing_box.left
        y = self._y_min + spacing_box.top
        width = (self._x_max - spacing_box.right) - x
        height = (self._y_max - spacing_box.bottom) - y
        return Rectangle(x=x, y=y, width=width, height=height)
