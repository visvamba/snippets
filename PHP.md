# PHP

## PHP error logging

Set in php.ini, create file, set ownership and permissions on file

On parent directory, `chmod o+rx <dir>`

## Foreach to insert HTML
```php+HTML
<table>
    <?php foreach($array as $key=>$value): ?>
    <tr>
        <td><?= $key; ?></td>
    </tr>
    <?php endforeach; ?>
</table>
```
or

```php+HTML
<table>
    <?php foreach($array as $value): ?>
    <tr>
        <td><?= $key; ?></td>
    </tr>
    <?php endforeach; ?>
</table>
```

